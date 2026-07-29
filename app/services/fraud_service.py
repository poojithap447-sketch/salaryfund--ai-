import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.ai_and_wellness import FraudAlert, FraudAlertStatus
from app.repositories.base import BaseRepository
from app.schemas.ai_and_wellness import FraudAlertResolve


class FraudAlertRepository(BaseRepository[FraudAlert]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, FraudAlert)

    async def list_open(self, offset: int = 0, limit: int = 50):
        result = await self.db.execute(
            select(FraudAlert).where(FraudAlert.status == FraudAlertStatus.OPEN).order_by(FraudAlert.created_at.desc()).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def list_for_employee(self, employee_id: uuid.UUID):
        result = await self.db.execute(select(FraudAlert).where(FraudAlert.employee_id == employee_id).order_by(FraudAlert.created_at.desc()))
        return result.scalars().all()


class FraudAlertService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = FraudAlertRepository(db)

    async def list_open_alerts(self, offset: int = 0, limit: int = 50):
        return await self.repo.list_open(offset, limit)

    async def list_for_employee(self, employee_id: uuid.UUID):
        return await self.repo.list_for_employee(employee_id)

    async def resolve_alert(self, alert_id: uuid.UUID, resolver_id: uuid.UUID, payload: FraudAlertResolve) -> FraudAlert:
        alert = await self.repo.get_by_id(alert_id)
        if not alert:
            raise NotFoundException("Fraud alert not found")

        alert.status = payload.status
        alert.resolution_notes = payload.resolution_notes
        alert.resolved_by_user_id = resolver_id
        alert.resolved_at = datetime.now(timezone.utc)

        await self.db.commit()
        await self.db.refresh(alert)
        return alert
