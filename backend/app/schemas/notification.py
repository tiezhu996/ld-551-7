from datetime import datetime

from pydantic import BaseModel

from app.constants.enums import NotificationType, UserRole


class NotificationCreate(BaseModel):
    title: str
    content: str
    type: NotificationType
    role: UserRole | None = None


class NotificationResponse(BaseModel):
    id: int
    title: str
    content: str
    type: NotificationType
    role: UserRole | None = None
    created_at: datetime
    is_read: bool = False

    model_config = {"from_attributes": True}


class NotificationMarkRead(BaseModel):
    notification_ids: list[int]


class UnreadCountResponse(BaseModel):
    count: int
