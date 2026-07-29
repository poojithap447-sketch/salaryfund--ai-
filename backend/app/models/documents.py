"""
Document management & KYC verification models.
"""
import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


class DocumentType(str, enum.Enum):
    PAN_CARD = "PAN_CARD"
    AADHAAR = "AADHAAR"
    SALARY_SLIP = "SALARY_SLIP"
    BANK_STATEMENT = "BANK_STATEMENT"
    OFFER_LETTER = "OFFER_LETTER"
    ADDRESS_PROOF = "ADDRESS_PROOF"
    SELFIE = "SELFIE"
    OTHER = "OTHER"


class DocumentStatus(str, enum.Enum):
    UPLOADED = "UPLOADED"
    OCR_PROCESSING = "OCR_PROCESSING"
    OCR_COMPLETE = "OCR_COMPLETE"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"
    FLAGGED_SUSPICIOUS = "FLAGGED_SUSPICIOUS"


class Document(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "documents"

    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), index=True)
    document_type: Mapped[DocumentType] = mapped_column(Enum(DocumentType, name="document_type_enum"), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_hash_sha256: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    mime_type: Mapped[str] = mapped_column(String(64), nullable=False)
    size_bytes: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[DocumentStatus] = mapped_column(Enum(DocumentStatus, name="document_status_enum"), default=DocumentStatus.UPLOADED)
    ocr_extracted_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    ocr_confidence: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    forgery_score: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    verified_by_user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(String(500), nullable=True)


class KYCStatus(str, enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING_REVIEW = "PENDING_REVIEW"
    VERIFIED = "VERIFIED"
    REJECTED = "REJECTED"


class KYC(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "kyc_records"

    employee_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), unique=True)
    status: Mapped[KYCStatus] = mapped_column(Enum(KYCStatus, name="kyc_status_enum"), default=KYCStatus.NOT_STARTED)
    pan_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    aadhaar_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    bank_account_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    liveness_check_passed: Mapped[bool] = mapped_column(Boolean, default=False)
    face_match_score: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    remarks: Mapped[str | None] = mapped_column(String(500), nullable=True)
