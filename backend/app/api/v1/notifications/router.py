import uuid

from fastapi import APIRouter, Query

from app.dependencies.auth import CurrentUser, DBSession
from app.schemas.ai_and_wellness import NotificationResponse
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("/me", response_model=list[NotificationResponse])
async def list_my_notifications(current_user: CurrentUser, db: DBSession, unread_only: bool = Query(False)):
    service = NotificationService(db)
    return await service.list_for_user(current_user.id, unread_only)


@router.post("/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(notification_id: uuid.UUID, current_user: CurrentUser, db: DBSession):
    service = NotificationService(db)
    return await service.mark_read(notification_id, current_user.id)
