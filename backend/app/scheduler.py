"""
Task Scheduler for automated jobs
Handles scheduled tasks like weekly email reports
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List
import logging

from app.database import SessionLocal
from app.models.field_activity import FieldActivity
from app.models.workspace import Workspace
from app.models.user import User
from app.services.field_activity_service import FieldActivityReportService
from app.services.push_notification_service import PushNotificationService
from app.config import settings

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def send_weekly_reports():
    """
    Send weekly activity reports for all workspaces
    Runs every Sunday at 5 PM (or configured day/time)
    """
    logger.info("Starting weekly report job...")

    if not settings.WEEKLY_REPORT_ENABLED:
        logger.info("Weekly reports disabled in settings")
        return

    # Removed early return - we still send individual reports to workspace members
    # even if weekly_report_recipients_list is empty

    db: Session = SessionLocal()

    try:
        # Calculate current week's date range (Monday to Sunday)
        today = datetime.now()
        days_since_monday = today.weekday()
        this_monday = today - timedelta(days=days_since_monday)
        this_sunday = this_monday + timedelta(days=6)

        date_from = this_monday.strftime("%Y-%m-%d")
        date_to = this_sunday.strftime("%Y-%m-%d")

        logger.info(f"Generating reports for period: {date_from} to {date_to}")

        # Get all active workspaces
        workspaces = db.query(Workspace).all()

        for workspace in workspaces:
            try:
                logger.info(f"Processing workspace: {workspace.name} (ID: {workspace.id})")

                # Get activities for this workspace
                activities = db.query(FieldActivity).filter(
                    FieldActivity.workspace_id == workspace.id,
                    FieldActivity.activity_date >= date_from,
                    FieldActivity.activity_date <= date_to
                ).order_by(
                    FieldActivity.activity_date,
                    FieldActivity.start_time
                ).all()

                if not activities:
                    logger.info(f"No activities found for workspace {workspace.name}")
                    continue

                # Send individual reports to each workspace member
                try:
                    result = await FieldActivityReportService.send_individual_reports(
                        workspace_id=workspace.id,
                        activities=activities,
                        date_from=date_from,
                        date_to=date_to,
                        db=db,
                        resend_api_key=settings.RESEND_API_KEY,
                        from_email=settings.RESEND_FROM_EMAIL,
                        from_name=settings.RESEND_FROM_NAME,
                        frontend_url=settings.FRONTEND_URL
                    )

                    logger.info(
                        f"Workspace {workspace.name}: {result['sent_count']} sent, "
                        f"{result['failed_count']} failed"
                    )

                    if result.get('errors'):
                        for error in result['errors']:
                            logger.error(f"  - {error}")

                except Exception as e:
                    logger.error(f"Failed to send individual reports for workspace {workspace.name}: {str(e)}")

                # Also send to configured recipients if specified (full report)
                if settings.weekly_report_recipients_list:
                    try:
                        await FieldActivityReportService.send_bulk_report(
                            activities=activities,
                            recipient_emails=settings.weekly_report_recipients_list,
                            date_from=date_from,
                            date_to=date_to,
                            resend_api_key=settings.RESEND_API_KEY,
                            from_email=settings.RESEND_FROM_EMAIL,
                            from_name=settings.RESEND_FROM_NAME,
                            frontend_url=settings.FRONTEND_URL
                        )
                        logger.info(f"Full report sent to configured recipients: {settings.weekly_report_recipients_list}")
                    except Exception as e:
                        logger.error(f"Failed to send to configured recipients: {str(e)}")

            except Exception as e:
                logger.error(f"Error processing workspace {workspace.id}: {str(e)}")
                continue

        logger.info("Weekly report job completed")

    except Exception as e:
        logger.error(f"Error in weekly report job: {str(e)}")
    finally:
        db.close()


async def send_weekly_push_notifications():
    """
    Send push notifications to all users about their weekly email report
    Runs every Monday at 8:00 AM
    """
    logger.info("Starting weekly push notification job...")

    if not settings.WEEKLY_REPORT_ENABLED:
        logger.info("Weekly push notifications skipped - reports disabled")
        return

    db: Session = SessionLocal()

    try:
        # Get all users
        users = db.query(User).all()

        sent_count = 0
        failed_count = 0

        for user in users:
            try:
                success = PushNotificationService.send_weekly_report_notification(
                    db=db,
                    user_id=user.id
                )
                if success:
                    sent_count += 1
                    logger.info(f"Push notification sent to {user.email}")
                else:
                    failed_count += 1

            except Exception as e:
                failed_count += 1
                logger.error(f"Failed to send push notification to user {user.id}: {str(e)}")

        logger.info(
            f"Weekly push notification job completed: {sent_count} sent, {failed_count} failed"
        )

    except Exception as e:
        logger.error(f"Error in weekly push notification job: {str(e)}")
    finally:
        db.close()


def start_scheduler():
    """
    Initialize and start the scheduler with configured jobs
    """
    if not settings.WEEKLY_REPORT_ENABLED:
        logger.info("Scheduler not started - weekly reports disabled")
        return

    # Add weekly report job
    # Runs on configured day of week at configured hour
    trigger = CronTrigger(
        day_of_week=settings.WEEKLY_REPORT_DAY,
        hour=settings.WEEKLY_REPORT_HOUR,
        minute=0,
        timezone=settings.WEEKLY_REPORT_TIMEZONE
    )

    scheduler.add_job(
        send_weekly_reports,
        trigger=trigger,
        id='weekly_reports',
        name='Send Weekly Activity Reports',
        replace_existing=True
    )

    # Add Monday 8 AM push notification job
    push_trigger = CronTrigger(
        day_of_week=0,  # Monday
        hour=8,
        minute=0,
        timezone=settings.WEEKLY_REPORT_TIMEZONE
    )

    scheduler.add_job(
        send_weekly_push_notifications,
        trigger=push_trigger,
        id='weekly_push_notifications',
        name='Send Weekly Push Notifications',
        replace_existing=True
    )

    scheduler.start()
    logger.info(
        f"Scheduler started - Weekly reports will run on "
        f"day {settings.WEEKLY_REPORT_DAY} at {settings.WEEKLY_REPORT_HOUR}:00 "
        f"{settings.WEEKLY_REPORT_TIMEZONE}"
    )
    logger.info(
        f"Push notifications will run every Monday at 8:00 AM {settings.WEEKLY_REPORT_TIMEZONE}"
    )


def shutdown_scheduler():
    """
    Gracefully shutdown the scheduler
    """
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shutdown")
