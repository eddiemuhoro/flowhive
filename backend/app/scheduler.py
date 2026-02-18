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
from app.models.workspace import Workspace, WorkspaceMember
from app.models.user import User, UserRole
from app.utils.email import send_activity_report_email
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
        workspaces = db.query(Workspace).filter(Workspace.is_active == True).all()

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

                # Get all workspace members with their user info
                members = db.query(WorkspaceMember, User).join(
                    User, WorkspaceMember.user_id == User.id
                ).filter(
                    WorkspaceMember.workspace_id == workspace.id
                ).all()

                # Group activities by staff for easy lookup
                activities_by_staff_id = {}
                all_activities_list = []

                for activity in activities:
                    staff_id = activity.support_staff_id
                    if staff_id not in activities_by_staff_id:
                        activities_by_staff_id[staff_id] = {
                            'staff_name': activity.support_staff.full_name or activity.support_staff.username,
                            'activities': [],
                            'total_hours': 0
                        }

                    activity_dict = {
                        'id': activity.id,
                        'title': activity.title,
                        'activity_date': str(activity.activity_date),
                        'start_time': str(activity.start_time) if activity.start_time else '',
                        'end_time': str(activity.end_time) if activity.end_time else '',
                        'duration_hours': activity.duration_hours,
                        'customer_name': activity.customer_name,
                        'location': activity.location,
                        'task_description': activity.task_description,
                        'remarks': activity.remarks,
                        'customer_rep': activity.customer_rep,
                    }

                    activities_by_staff_id[staff_id]['activities'].append(activity_dict)
                    activities_by_staff_id[staff_id]['total_hours'] += activity.duration_hours or 0

                all_activities_list = list(activities_by_staff_id.values())

                # Calculate full summary for managers/executives
                total_hours = sum(a.duration_hours or 0 for a in activities)
                unique_customers = len(set(a.customer_name for a in activities))
                unique_staff = len(activities_by_staff_id)

                full_summary = {
                    'total_activities': len(activities),
                    'total_hours': total_hours,
                    'unique_customers': unique_customers,
                    'unique_staff': unique_staff
                }

                sent_count = 0
                failed_count = 0

                # Send individual reports to each member
                for member, user in members:
                    if not user.email:
                        continue  # Skip users without email

                    try:
                        # Check user role
                        is_manager_or_exec = user.role in [UserRole.MANAGER, UserRole.EXECUTIVE]

                        if is_manager_or_exec:
                            # Send full report to managers/executives
                            subject = f"Weekly Activity Report - {workspace.name} All Staff ({date_from} to {date_to})"
                            activities_to_send = all_activities_list
                            summary_to_send = full_summary
                            logger.info(f"Sending full report to {user.email} ({user.role})")
                        else:
                            # Send only their activities to team members
                            user_activities = activities_by_staff_id.get(user.id)

                            if not user_activities:
                                # No activities for this user, skip
                                logger.info(f"No activities for {user.email}, skipping")
                                continue

                            subject = f"Your Weekly Activity Report - {workspace.name} ({date_from} to {date_to})"
                            activities_to_send = [user_activities]
                            summary_to_send = {
                                'total_activities': len(user_activities['activities']),
                                'total_hours': user_activities['total_hours'],
                                'unique_customers': len(set(a['customer_name'] for a in user_activities['activities'])),
                                'unique_staff': 1
                            }
                            logger.info(f"Sending individual report to {user.email}")

                        # Send email
                        result = send_activity_report_email(
                            to_emails=[user.email],
                            subject=subject,
                            activities_by_staff=activities_to_send,
                            date_from=date_from,
                            date_to=date_to,
                            summary=summary_to_send,
                            resend_api_key=settings.RESEND_API_KEY,
                            from_email=settings.RESEND_FROM_EMAIL,
                            from_name=settings.RESEND_FROM_NAME,
                            frontend_url=settings.FRONTEND_URL
                        )

                        if result['success']:
                            sent_count += 1
                        else:
                            failed_count += 1
                            logger.error(f"Failed to send to {user.email}: {result.get('error')}")

                    except Exception as e:
                        failed_count += 1
                        logger.error(f"Error sending to {user.email}: {str(e)}")

                # Also send to configured recipients if specified
                if settings.weekly_report_recipients_list:
                    try:
                        subject = f"Weekly Activity Report - {workspace.name} All Staff ({date_from} to {date_to})"
                        result = send_activity_report_email(
                            to_emails=settings.weekly_report_recipients_list,
                            subject=subject,
                            activities_by_staff=all_activities_list,
                            date_from=date_from,
                            date_to=date_to,
                            summary=full_summary,
                            resend_api_key=settings.RESEND_API_KEY,
                            from_email=settings.RESEND_FROM_EMAIL,
                            from_name=settings.RESEND_FROM_NAME,
                            frontend_url=settings.FRONTEND_URL
                        )
                        if result['success']:
                            logger.info(f"Report sent to configured recipients")
                    except Exception as e:
                        logger.error(f"Failed to send to configured recipients: {str(e)}")

                logger.info(f"Workspace {workspace.name}: {sent_count} sent, {failed_count} failed")

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
