"""
Document upload, storage, OCR extraction, and forgery-screening service.
Files are hashed (SHA-256) at upload time for duplicate-detection and audit,
stored on disk (or S3-compatible object storage - see settings.UPLOAD_DIR),
and processed through the OCR + forgery pipeline synchronously for
small documents or via Celery for larger batches.
"""
import hashlib
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import FileUploadException, NotFoundException
from app.models.documents import Document, DocumentStatus, DocumentType
from app.repositories.base import BaseRepository
from app.utils.ocr import compute_forgery_score, extract_pan_fields


class DocumentRepository(BaseRepository[Document]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Document)

    async def list_for_employee(self, employee_id: uuid.UUID):
        result = await self.db.execute(select(Document).where(Document.employee_id == employee_id))
        return result.scalars().all()

    async def find_by_hash(self, file_hash: str):
        result = await self.db.execute(select(Document).where(Document.file_hash_sha256 == file_hash))
        return result.scalars().all()


class DocumentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = DocumentRepository(db)

    async def upload_document(
        self, employee_id: uuid.UUID, document_type: DocumentType, filename: str, content: bytes, mime_type: str
    ) -> Document:
        max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
        if len(content) > max_bytes:
            raise FileUploadException(f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_MB}MB")
        if mime_type not in settings.ALLOWED_DOCUMENT_TYPES:
            raise FileUploadException(f"File type {mime_type} is not permitted. Allowed: {settings.ALLOWED_DOCUMENT_TYPES}")

        file_hash = hashlib.sha256(content).hexdigest()

        upload_dir = Path(settings.UPLOAD_DIR) / str(employee_id)
        upload_dir.mkdir(parents=True, exist_ok=True)
        safe_name = f"{uuid.uuid4().hex}_{Path(filename).suffix}"
        file_path = upload_dir / safe_name
        file_path.write_bytes(content)

        document = await self.repo.create(
            employee_id=employee_id,
            document_type=document_type,
            file_path=str(file_path),
            file_hash_sha256=file_hash,
            mime_type=mime_type,
            size_bytes=len(content),
            status=DocumentStatus.UPLOADED,
        )
        await self.db.commit()
        await self.db.refresh(document)

        # Synchronous OCR + forgery scoring for images (small/fast); PDFs are queued via Celery in production.
        if mime_type.startswith("image/"):
            await self._process_ocr(document, content)

        return document

    async def _process_ocr(self, document: Document, content: bytes) -> Document:
        document.status = DocumentStatus.OCR_PROCESSING
        await self.db.commit()

        try:
            forgery_score = compute_forgery_score(content)
            extracted = extract_pan_fields(content) if document.document_type == DocumentType.PAN_CARD else {
                "raw_text": None,
                "extraction_confidence": None,
            }

            document.forgery_score = forgery_score
            document.ocr_extracted_data = extracted
            document.ocr_confidence = extracted.get("extraction_confidence")
            document.status = DocumentStatus.FLAGGED_SUSPICIOUS if forgery_score > 0.6 else DocumentStatus.OCR_COMPLETE
        except Exception as exc:
            document.status = DocumentStatus.UPLOADED
            document.rejection_reason = f"OCR processing failed: {exc}"

        await self.db.commit()
        await self.db.refresh(document)
        return document

    async def verify_document(self, document_id: uuid.UUID, reviewer_id: uuid.UUID, approve: bool, reason: str | None = None) -> Document:
        document = await self.repo.get_by_id(document_id)
        if not document:
            raise NotFoundException("Document not found")
        document.status = DocumentStatus.VERIFIED if approve else DocumentStatus.REJECTED
        document.verified_by_user_id = reviewer_id
        document.verified_at = datetime.now(timezone.utc)
        document.rejection_reason = reason
        await self.db.commit()
        await self.db.refresh(document)
        return document

    async def list_for_employee(self, employee_id: uuid.UUID):
        return await self.repo.list_for_employee(employee_id)
