from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.constants.enums import UserRole
from app.models.notification import Notification, NotificationRead
from app.models.user import User
from app.schemas.notification import NotificationCreate, NotificationResponse


class NotificationService:
    @staticmethod
    def create(db: Session, payload: NotificationCreate) -> Notification:
        notification = Notification(
            title=payload.title,
            content=payload.content,
            type=payload.type,
            role=payload.role,
        )
        db.add(notification)
        db.commit()
        db.refresh(notification)
        return notification

    @staticmethod
    def list_by_user(db: Session, user: User, page: int = 1, size: int = 20) -> tuple[list[NotificationResponse], int]:
        read_ids_query = db.query(NotificationRead.notification_id).filter(NotificationRead.user_id == user.id)
        query = db.query(Notification).filter(
            or_(Notification.role.is_(None), Notification.role == user.role)
        )
        total = query.count()
        notifications = (
            query.order_by(Notification.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
            .all()
        )
        read_ids = {r[0] for r in read_ids_query.all()}
        result = []
        for n in notifications:
            resp = NotificationResponse.model_validate(n)
            resp.is_read = n.id in read_ids
            result.append(resp)
        return result, total

    @staticmethod
    def mark_read(db: Session, user: User, notification_ids: list[int]) -> None:
        existing = db.query(NotificationRead.notification_id).filter(
            NotificationRead.user_id == user.id,
            NotificationRead.notification_id.in_(notification_ids),
        ).all()
        existing_ids = {r[0] for r in existing}
        to_create = [nid for nid in notification_ids if nid not in existing_ids]
        for nid in to_create:
            db.add(NotificationRead(user_id=user.id, notification_id=nid))
        db.commit()

    @staticmethod
    def mark_all_read(db: Session, user: User) -> None:
        unread_notifications = (
            db.query(Notification.id)
            .outerjoin(NotificationRead, (NotificationRead.notification_id == Notification.id) & (NotificationRead.user_id == user.id))
            .filter(
                or_(Notification.role.is_(None), Notification.role == user.role),
                NotificationRead.notification_id.is_(None),
            )
            .all()
        )
        for (nid,) in unread_notifications:
            db.add(NotificationRead(user_id=user.id, notification_id=nid))
        db.commit()

    @staticmethod
    def get_unread_count(db: Session, user: User) -> int:
        return (
            db.query(Notification)
            .outerjoin(NotificationRead, (NotificationRead.notification_id == Notification.id) & (NotificationRead.user_id == user.id))
            .filter(
                or_(Notification.role.is_(None), Notification.role == user.role),
                NotificationRead.notification_id.is_(None),
            )
            .count()
        )
