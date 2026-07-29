import uuid
from datetime import date

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel

from app.dependencies.auth import DBSession, require_roles
from app.models.loans import InterestRate, Lender
from app.repositories.loan_repository import LenderRepository

router = APIRouter(prefix="/lenders", tags=["Lenders"])


class LenderCreate(BaseModel):
    name: str
    license_number: str
    contact_email: str
    max_exposure_limit: float = 0


class InterestRateCreate(BaseModel):
    lender_id: uuid.UUID
    loan_type_id: uuid.UUID
    risk_band: str
    annual_rate_pct: float
    processing_fee_pct: float = 1.0
    effective_from: date


@router.post("", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("PLATFORM_ADMIN"))])
async def onboard_lender(payload: LenderCreate, db: DBSession):
    repo = LenderRepository(db)
    lender = await repo.create(**payload.model_dump())
    await db.commit()
    return {"id": str(lender.id), "name": lender.name}


@router.get("", response_model=list[dict])
async def list_lenders(db: DBSession):
    repo = LenderRepository(db)
    lenders = await repo.list_active()
    return [{"id": str(l.id), "name": l.name, "is_active": l.is_active} for l in lenders]


@router.post("/interest-rates", status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_roles("PLATFORM_ADMIN", "LENDER"))])
async def add_interest_rate(payload: InterestRateCreate, db: DBSession):
    rate = InterestRate(**payload.model_dump())
    db.add(rate)
    await db.commit()
    await db.refresh(rate)
    return {"id": str(rate.id), "annual_rate_pct": float(rate.annual_rate_pct)}
