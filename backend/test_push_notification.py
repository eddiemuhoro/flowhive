"""
Test script to send push notification
Run: python test_push_notification.py
"""

from app.database import SessionLocal
from app.services.push_notification_service import PushNotificationService

def test_push_notification():
    db = SessionLocal()

    try:
        # Test notification for user ID 9 (eddiemuhoro@gmail.com)
        user_id = 9

        print(f"Sending test push notification to user {user_id}...")

        result = PushNotificationService.send_notification(
            db=db,
            user_id=user_id,
            title="🎉 Test Notification",
            message="This is a test push notification from Flowhive!",
            data={
                "url": "/field",
                "tag": "test-notification"
            }
        )

        if result:
            print("✅ Push notification sent successfully!")
            print("Check your browser - you should see the notification")
        else:
            print("❌ Failed to send push notification")
            print("Make sure:")
            print("1. Browser is open")
            print("2. Service worker is active")
            print("3. Notification permission is granted")

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_push_notification()
