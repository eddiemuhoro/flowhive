"""
Push Notification Service
Handles sending web push notifications to users
"""

from pywebpush import webpush, WebPushException
from py_vapid import Vapid
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import json
import logging
import tempfile
import os

from app.models.push_subscription import PushSubscription
from app.models.user import User
from app.config import settings

logger = logging.getLogger(__name__)


class PushNotificationService:
    """Service for sending push notifications"""

    _vapid_instance = None

    @staticmethod
    def _normalize_private_key_pem(raw_key: str) -> str:
        """Normalize VAPID private key loaded from environment.

        Handles common .env formatting issues like surrounding quotes and
        escaped newlines ("\\n") so py_vapid can parse the PEM correctly.
        """
        key = (raw_key or "").strip()

        if not key:
            return ""

        # Remove wrapping quotes if present.
        if (key.startswith('"') and key.endswith('"')) or (
            key.startswith("'") and key.endswith("'")
        ):
            key = key[1:-1]

        # Convert escaped newlines from .env into real line breaks.
        if "\\n" in key:
            key = key.replace("\\n", "\n")

        # Ensure trailing newline so PEM parser sees final marker cleanly.
        if not key.endswith("\n"):
            key += "\n"

        return key

    @classmethod
    def _get_vapid(cls):
        """Get or create VAPID instance"""
        if cls._vapid_instance is None:
            private_key_pem = cls._normalize_private_key_pem(settings.VAPID_PRIVATE_KEY)
            if not private_key_pem:
                raise ValueError("VAPID_PRIVATE_KEY is empty or missing")

            # Write private key to temporary file and load from there
            # This workaround is needed because Vapid.from_string() doesn't handle PEM format correctly
            with tempfile.NamedTemporaryFile(mode='w', suffix='.pem', delete=False) as f:
                f.write(private_key_pem)
                temp_path = f.name

            try:
                cls._vapid_instance = Vapid.from_file(temp_path)
            except Exception as e:
                logger.error("Failed to load VAPID private key. Check backend/.env VAPID_PRIVATE_KEY PEM formatting: %s", e)
                raise
            finally:
                os.unlink(temp_path)

        return cls._vapid_instance

    @staticmethod
    def send_notification(
        db: Session,
        user_id: int,
        title: str,
        message: str,
        data: Dict[str, Any] = None
    ) -> bool:
        """
        Send push notification to a specific user

        Args:
            db: Database session
            user_id: User to notify
            title: Notification title
            message: Notification message
            data: Additional data (url, tag, etc.)

        Returns:
            True if sent successfully, False otherwise
        """
        # Get all active subscriptions for this user
        subscriptions = db.query(PushSubscription).filter(
            PushSubscription.user_id == user_id,
            PushSubscription.active == True
        ).all()

        if not subscriptions:
            logger.warning(f"No active push subscriptions for user {user_id}")
            return False

        # Prepare notification payload
        payload = {
            "title": title,
            "message": message,
            "icon": "/icon-192x192.svg",
            "badge": "/icon-192x192.svg",
        }

        if data:
            payload.update(data)

        success_count = 0

        for subscription in subscriptions:
            try:
                # Get VAPID instance
                vapid = PushNotificationService._get_vapid()

                # Send push notification
                webpush(
                    subscription_info={
                        "endpoint": subscription.endpoint,
                        "keys": {
                            "p256dh": subscription.p256dh_key,
                            "auth": subscription.auth_key
                        }
                    },
                    data=json.dumps(payload),
                    vapid_private_key=vapid,
                    vapid_claims={
                        "sub": f"mailto:{settings.VAPID_CLAIM_EMAIL}"
                    }
                )
                success_count += 1
                logger.info(f"Push notification sent to user {user_id}")

            except WebPushException as e:
                logger.error(f"Failed to send push notification: {e}")

                # If subscription is invalid/expired, deactivate it
                if e.response and e.response.status_code in [404, 410]:
                    subscription.active = False
                    db.commit()
                    logger.info(f"Deactivated invalid subscription for user {user_id}")

        return success_count > 0

    @staticmethod
    def send_to_workspace(
        db: Session,
        workspace_id: int,
        title: str,
        message: str,
        data: Dict[str, Any] = None
    ) -> int:
        """
        Send push notification to all users in a workspace

        Returns:
            Number of users notified
        """
        from app.models.workspace import WorkspaceMember

        members = db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == workspace_id
        ).all()

        success_count = 0
        for member in members:
            if PushNotificationService.send_notification(db, member.user_id, title, message, data):
                success_count += 1

        return success_count

    @staticmethod
    def send_weekly_report_notification(db: Session, user_id: int) -> bool:
        """Send notification about weekly email report"""
        return PushNotificationService.send_notification(
            db=db,
            user_id=user_id,
            title="📊 Weekly Report Ready",
            message="Your personalized weekly activity report has been sent to your email.",
            data={
                "tag": "weekly-report",
                "url": "/field"
            }
        )
