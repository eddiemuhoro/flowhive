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
from app.services.field_activity_service import FieldActivityReportService
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

    if not settings.weekly_report_recipients_list:
        logger.warning("No recipients configured for weekly reports")
        return

    db: Session = SessionLocal()

    try:
        # Calculate last week's date range (Monday to Sunday)
        today = datetime.now()
        days_since_monday = today.weekday()
        last_monday = today - timedelta(days=days_since_monday + 7)
        last_sunday = last_monday + timedelta(days=6)

        date_from = last_monday.strftime("%Y-%m-%d")
        date_to = last_sunday.strftime("%Y-%m-%d")

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

    scheduler.start()
    logger.info(
        f"Scheduler started - Weekly reports will run on "
        f"day {settings.WEEKLY_REPORT_DAY} at {settings.WEEKLY_REPORT_HOUR}:00 "
        f"{settings.WEEKLY_REPORT_TIMEZONE}"
    )


def shutdown_scheduler():
    """
    Gracefully shutdown the scheduler
    """
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler shutdown")
