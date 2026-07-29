import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.documents import DocumentStatus, DocumentType


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    employee_id: uuid.UUID
    document_type: DocumentType
    status: DocumentStatus
    ocr_confidence: float | None
    forgery_score: float | None
    created_at: datetime


class DocumentVerifyRequest(BaseModel):
    approve: bool
    rejection_reason: str | None = None
