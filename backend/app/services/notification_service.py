import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundException
from app.models.ai_and_wellness import Notification, NotificationChannel, NotificationStatus
from app.repositories.base import BaseRepository
from app.background_tasks.notification_tasks import send_email_task, send_sms_task


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, db: AsyncSession):
        super().__init__(db, Notification)

    async def list_for_user(self, user_id: uuid.UUID, offset: int = 0, limit: int = 50):
        result = await self.db.execute(
            select(Notification).where(Notification.user_id == user_id).order_by(Notification.created_at.desc()).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def unread_count(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(Notification).where(Notification.user_id == user_id, Notification.status != NotificationStatus.READ)
        )
        return len(result.scalars().all())


class NotificationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = NotificationRepository(db)

    async def notify(
        self,
        user_id: uuid.UUID,
        channel: NotificationChannel,
        template_code: str,
        title: str,
        body: str,
        recipient_email: str | None = None,
        recipient_phone: str | None = None,
    ) -> Notification:
        notification = await self.repo.create(
            user_id=user_id, channel=channel, template_code=template_code, title=title, body=body, status=NotificationStatus.PENDING
        )
        await self.db.commit()
        await self.db.refresh(notification)

        if channel == NotificationChannel.EMAIL and recipient_email:
            send_email_task.delay(to_email=recipient_email, subject=title, body=body)
        elif channel == NotificationChannel.SMS and recipient_phone:
            send_sms_task.delay(to_phone=recipient_phone, message=body)

        notification.status = NotificationStatus.SENT
        notification.sent_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(notification)
        return notification

    async def list_for_user(self, user_id: uuid.UUID, offset: int = 0, limit: int = 50):
        return await self.repo.list_for_user(user_id, offset, limit)

    async def mark_read(self, notification_id: uuid.UUID, user_id: uuid.UUID) -> Notification:
        notification = await self.repo.get_by_id(notification_id)
        if not notification or notification.user_id != user_id:
            raise NotFoundException("Notification not found")
        notification.status = NotificationStatus.READ
        notification.read_at = datetime.now(timezone.utc)
        await self.db.commit()
        await self.db.refresh(notification)
        return notification
