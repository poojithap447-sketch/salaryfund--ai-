import uuid

from fastapi import APIRouter

from app.dependencies.auth import CurrentUser, DBSession
from app.repositories.loan_repository import EMIRepository
from app.schemas.loans import EMIPaymentRequest, EMIResponse
from app.services.loan_service import LoanApplicationService

router = APIRouter(prefix="/emi", tags=["EMI"])


@router.get("/loan/{loan_id}", response_model=list[EMIResponse])
async def list_emis_for_loan(loan_id: uuid.UUID, db: DBSession):
    repo = EMIRepository(db)
    return await repo.list_for_loan(loan_id)


@router.post("/pay", response_model=EMIResponse)
async def pay_emi(payload: EMIPaymentRequest, current_user: CurrentUser, db: DBSession):
    """Records an EMI payment (integrate with your payment gateway webhook to call this)."""
    service = LoanApplicationService(db)
    return await service.pay_emi(payload.emi_id, payload.amount, payload.payment_gateway_ref)
