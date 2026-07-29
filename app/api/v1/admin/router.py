import uuid

from fastapi import APIRouter, Depends, Query

from app.dependencies.auth import CurrentUser, DBSession, require_roles
from app.schemas.ai_and_wellness import FraudAlertResolve, FraudAlertResponse
from app.services.fraud_service import FraudAlertService

router = APIRouter(prefix="/admin", tags=["Admin & Fraud Alerts"], dependencies=[Depends(require_roles("PLATFORM_ADMIN", "SUPPORT"))])


@router.get("/fraud-alerts", response_model=list[FraudAlertResponse])
async def list_open_fraud_alerts(db: DBSession, offset: int = Query(0, ge=0), limit: int = Query(50, le=200)):
    service = FraudAlertService(db)
    return await service.list_open_alerts(offset, limit)


@router.get("/fraud-alerts/employee/{employee_id}", response_model=list[FraudAlertResponse])
async def list_employee_fraud_alerts(employee_id: uuid.UUID, db: DBSession):
    service = FraudAlertService(db)
    return await service.list_for_employee(employee_id)


@router.post("/fraud-alerts/{alert_id}/resolve", response_model=FraudAlertResponse)
async def resolve_fraud_alert(alert_id: uuid.UUID, payload: FraudAlertResolve, current_user: CurrentUser, db: DBSession):
    service = FraudAlertService(db)
    return await service.resolve_alert(alert_id, current_user.id, payload)
