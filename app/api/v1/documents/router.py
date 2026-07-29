import uuid

from fastapi import APIRouter, Depends, File, Form, UploadFile

from app.dependencies.auth import CurrentUser, DBSession, require_roles
from app.models.documents import DocumentType
from app.schemas.documents import DocumentResponse, DocumentVerifyRequest
from app.services.document_service import DocumentService
from app.services.organization_service import EmployeeService

router = APIRouter(prefix="/documents", tags=["Documents & OCR"])


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    current_user: CurrentUser,
    db: DBSession,
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
):
    """
    Uploads a KYC/salary-slip document. For image files (PNG/JPEG) this
    synchronously runs OCR (OpenCV preprocessing + pytesseract) to extract
    PAN/Aadhaar numbers and computes a forgery heuristic score that feeds
    the Fraud Detection Engine.
    """
    employee_service = EmployeeService(db)
    employee = await employee_service.get_employee_by_user(current_user)
    content = await file.read()
    service = DocumentService(db)
    return await service.upload_document(employee.id, document_type, file.filename, content, file.content_type)


@router.get("/me", response_model=list[DocumentResponse])
async def list_my_documents(current_user: CurrentUser, db: DBSession):
    employee_service = EmployeeService(db)
    employee = await employee_service.get_employee_by_user(current_user)
    service = DocumentService(db)
    return await service.list_for_employee(employee.id)


@router.post(
    "/{document_id}/verify",
    response_model=DocumentResponse,
    dependencies=[Depends(require_roles("PLATFORM_ADMIN", "SUPPORT"))],
)
async def verify_document(document_id: uuid.UUID, payload: DocumentVerifyRequest, current_user: CurrentUser, db: DBSession):
    service = DocumentService(db)
    return await service.verify_document(document_id, current_user.id, payload.approve, payload.rejection_reason)
