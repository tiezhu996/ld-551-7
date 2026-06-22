from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_role
from app.constants.enums import UserRole
from app.core.database import get_db
from app.models.user import User
from app.schemas.common import PageResponse
from app.schemas.notification import (
    NotificationCreate,
    NotificationMarkRead,
    NotificationResponse,
    UnreadCountResponse,
)
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=PageResponse[NotificationResponse])
def list_notifications(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    items, total = NotificationService.list_by_user(db, user, page, size)
    return PageResponse(total=total, page=page, size=size, items=items)


@router.get("/unread-count", response_model=UnreadCountResponse)
def get_unread_count(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    count = NotificationService.get_unread_count(db, user)
    return UnreadCountResponse(count=count)


@router.post("/mark-read", status_code=204)
def mark_read(
    payload: NotificationMarkRead,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    NotificationService.mark_read(db, user, payload.notification_ids)


@router.post("/mark-all-read", status_code=204)
def mark_all_read(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    NotificationService.mark_all_read(db, user)


@router.post("", response_model=NotificationResponse, status_code=201)
def create_notification(
    payload: NotificationCreate,
    user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    return NotificationService.create(db, payload)
