"""
Field Activity Service
Business logic for field activity operations, including report generation and distribution
"""

from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.field_activity import FieldActivity
from app.models.workspace import WorkspaceMember
from app.models.user import User, UserRole
from app.utils.email import send_activity_report_email


class FieldActivityReportService:
    """Service for handling field activity report generation and distribution"""

    @staticmethod
    def _convert_activity_to_dict(activity: FieldActivity) -> Dict[str, Any]:
        """Convert a FieldActivity model to a dictionary for email template"""
        return {
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

    @staticmethod
    def _group_activities_by_staff(activities: List[FieldActivity]) -> Dict[int, Dict[str, Any]]:
        """Group activities by staff member ID"""
        activities_by_staff = {}

        for activity in activities:
            staff_id = activity.support_staff_id
            if staff_id not in activities_by_staff:
                activities_by_staff[staff_id] = {
                    'staff_name': activity.support_staff.full_name or activity.support_staff.username,
                    'activities': [],
                    'total_hours': 0
                }

            activity_dict = FieldActivityReportService._convert_activity_to_dict(activity)
            activities_by_staff[staff_id]['activities'].append(activity_dict)
            activities_by_staff[staff_id]['total_hours'] += activity.duration_hours or 0

        return activities_by_staff

    @staticmethod
    def _calculate_summary(activities: List[FieldActivity], activities_by_staff: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate summary statistics for activities"""
        total_hours = sum(a.duration_hours or 0 for a in activities)
        unique_customers = len(set(a.customer_name for a in activities))
        unique_staff = len(activities_by_staff)

        return {
            'total_activities': len(activities),
            'total_hours': total_hours,
            'unique_customers': unique_customers,
            'unique_staff': unique_staff
        }

    @staticmethod
    async def send_bulk_report(
        activities: List[FieldActivity],
        recipient_emails: List[str],
        date_from: str,
        date_to: str,
        resend_api_key: str,
        from_email: str,
        from_name: str,
        frontend_url: str
    ) -> Dict[str, Any]:
        """
        Send the same full report to all specified recipients

        Args:
            activities: List of field activities to include
            recipient_emails: List of email addresses to send to
            date_from: Start date of report period
            date_to: End date of report period
            resend_api_key: API key for Resend service
            from_email: Sender email address
            from_name: Sender display name
            frontend_url: URL of frontend application

        Returns:
            Dict with message and email_id

        Raises:
            HTTPException: If email sending fails
        """
        # Group activities by staff
        activities_by_staff = FieldActivityReportService._group_activities_by_staff(activities)
        activities_list = list(activities_by_staff.values())

        # Calculate summary
        summary = FieldActivityReportService._calculate_summary(activities, activities_by_staff)

        # Generate subject
        subject = f"Weekly Activity Report - {date_from} to {date_to}"

        # Send email
        result = send_activity_report_email(
            to_emails=recipient_emails,
            subject=subject,
            activities_by_staff=activities_list,
            date_from=date_from,
            date_to=date_to,
            summary=summary,
            resend_api_key=resend_api_key,
            from_email=from_email,
            from_name=from_name,
            frontend_url=frontend_url
        )

        if not result['success']:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get('error', 'Failed to send email')
            )

        return {
            'message': result['message'],
            'email_id': result.get('email_id')
        }

    @staticmethod
    async def send_individual_reports(
        workspace_id: int,
        activities: List[FieldActivity],
        date_from: str,
        date_to: str,
        db: Session,
        resend_api_key: str,
        from_email: str,
        from_name: str,
        frontend_url: str
    ) -> Dict[str, Any]:
        """
        Send personalized reports to each staff member
        - Team members get only their activities
        - Managers/Executives get full reports

        Args:
            workspace_id: ID of the workspace
            activities: List of all field activities
            date_from: Start date of report period
            date_to: End date of report period
            db: Database session
            resend_api_key: API key for Resend service
            from_email: Sender email address
            from_name: Sender display name
            frontend_url: URL of frontend application

        Returns:
            Dict with sent_count, failed_count, and errors

        Raises:
            HTTPException: If no members found in workspace
        """
        # Get all workspace members with their user info
        members = db.query(WorkspaceMember, User).join(
            User, WorkspaceMember.user_id == User.id
        ).filter(
            WorkspaceMember.workspace_id == workspace_id
        ).all()

        if not members:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No members found in workspace"
            )

        # Group activities by staff for easy lookup
        activities_by_staff_id = FieldActivityReportService._group_activities_by_staff(activities)
        all_activities_list = list(activities_by_staff_id.values())

        # Calculate full summary for managers/executives
        full_summary = FieldActivityReportService._calculate_summary(activities, activities_by_staff_id)

        sent_count = 0
        failed_count = 0
        errors = []

        # Send reports to each member
        for member, user in members:
            if not user.email:
                continue  # Skip users without email

            try:
                # Check user role
                is_manager_or_exec = user.role in [UserRole.MANAGER, UserRole.EXECUTIVE]

                if is_manager_or_exec:
                    # Send full report to managers/executives
                    subject = f"Weekly Activity Report - All Staff ({date_from} to {date_to})"
                    activities_to_send = all_activities_list
                    summary_to_send = full_summary
                else:
                    # Send only their activities to team members
                    user_activities = activities_by_staff_id.get(user.id)

                    if not user_activities:
                        # No activities for this user, skip
                        continue

                    subject = f"Your Weekly Activity Report ({date_from} to {date_to})"
                    activities_to_send = [user_activities]
                    summary_to_send = {
                        'total_activities': len(user_activities['activities']),
                        'total_hours': user_activities['total_hours'],
                        'unique_customers': len(set(a['customer_name'] for a in user_activities['activities'])),
                        'unique_staff': 1
                    }

                # Send email
                result = send_activity_report_email(
                    to_emails=[user.email],
                    subject=subject,
                    activities_by_staff=activities_to_send,
                    date_from=date_from,
                    date_to=date_to,
                    summary=summary_to_send,
                    resend_api_key=resend_api_key,
                    from_email=from_email,
                    from_name=from_name,
                    frontend_url=frontend_url
                )

                if result['success']:
                    sent_count += 1
                else:
                    failed_count += 1
                    errors.append(f"{user.email}: {result.get('error', 'Unknown error')}")

            except Exception as e:
                failed_count += 1
                errors.append(f"{user.email}: {str(e)}")

        return {
            'message': f'Individual reports sent to {sent_count} member(s)',
            'sent_count': sent_count,
            'failed_count': failed_count,
            'errors': errors if errors else None
        }
