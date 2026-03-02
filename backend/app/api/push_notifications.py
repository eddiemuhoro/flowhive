"""
Push Notification API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List

from app.database import get_db
from app.models.user import User
from app.models.push_subscription import PushSubscription
from app.services.push_notification_service import PushNotificationService
from app.utils.auth import get_current_active_user

router = APIRouter()


class PushSubscriptionCreate(BaseModel):
    endpoint: str
    keys: dict  # Contains p256dh and auth


class PushSubscriptionResponse(BaseModel):
    id: int
    active: bool

    class Config:
        from_attributes = True


@router.post("/subscribe", response_model=PushSubscriptionResponse)
async def subscribe_to_push(
    subscription: PushSubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Subscribe current user to push notifications
    """
    # Check if subscription already exists
    existing = db.query(PushSubscription).filter(
        PushSubscription.endpoint == subscription.endpoint
    ).first()

    if existing:
        # Reactivate if it was deactivated
        existing.active = True
        existing.user_id = current_user.id
        db.commit()
        db.refresh(existing)
        return existing

    # Create new subscription
    new_subscription = PushSubscription(
        user_id=current_user.id,
        endpoint=subscription.endpoint,
        p256dh_key=subscription.keys.get("p256dh", ""),
        auth_key=subscription.keys.get("auth", ""),
        active=True
    )

    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    return new_subscription


@router.delete("/unsubscribe")
async def unsubscribe_from_push(
    endpoint: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Unsubscribe from push notifications
    """
    subscription = db.query(PushSubscription).filter(
        PushSubscription.endpoint == endpoint,
        PushSubscription.user_id == current_user.id
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )

    subscription.active = False
    db.commit()

    return {"message": "Unsubscribed successfully"}


@router.get("/vapid-public-key")
async def get_vapid_public_key():
    """
    Get VAPID public key for push subscription
    """
    from app.config import settings

    if not settings.VAPID_PUBLIC_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Push notifications not configured"
        )

    return {"publicKey": settings.VAPID_PUBLIC_KEY}


@router.get("/subscription-status")
async def get_subscription_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Check if current user has active push subscription
    """
    subscription = db.query(PushSubscription).filter(
        PushSubscription.user_id == current_user.id,
        PushSubscription.active == True
    ).first()

    return {
        "subscribed": subscription is not None,
        "count": db.query(PushSubscription).filter(
            PushSubscription.user_id == current_user.id,
            PushSubscription.active == True
        ).count()
    }


class SendNotificationRequest(BaseModel):
    title: str
    body: str
    user_ids: Optional[List[int]] = None  # If None, send to all active users
    icon: Optional[str] = None
    url: Optional[str] = None


@router.post("/send")
async def send_notification(
    notification: SendNotificationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Send push notification to specified users or all active users
    """
    # Determine recipients
    if notification.user_ids:
        users = db.query(User).filter(
            User.id.in_(notification.user_ids),
            User.is_active == True
        ).all()
    else:
        users = db.query(User).filter(User.is_active == True).all()

    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active users found"
        )

    # Send notifications
    success_count = 0
    failed_count = 0
    results = []

    for user in users:
        try:
            # Prepare additional data
            data = {}
            if notification.icon:
                data["icon"] = notification.icon
            if notification.url:
                data["url"] = notification.url

            result = PushNotificationService.send_notification(
                db=db,
                user_id=user.id,
                title=notification.title,
                message=notification.body,
                data=data if data else None
            )
            if result:
                success_count += 1
                results.append({"user_id": user.id, "status": "sent"})
            else:
                failed_count += 1
                results.append({"user_id": user.id, "status": "failed"})
        except Exception as e:
            failed_count += 1
            results.append({"user_id": user.id, "status": "error", "message": str(e)})

    return {
        "message": f"Notifications sent to {success_count} user(s), {failed_count} failed",
        "total_users": len(users),
        "success_count": success_count,
        "failed_count": failed_count,
        "results": results
    }
