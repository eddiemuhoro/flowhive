"""
Diagnostic script to check weekly report scheduler setup
Run with: python check_scheduler_setup.py
"""

import os
from dotenv import load_dotenv
from app.database import SessionLocal
from app.models.workspace import Workspace, WorkspaceMember
from app.models.user import User
from sqlalchemy.orm import joinedload

load_dotenv()

def check_environment():
    """Check required environment variables"""
    print("=" * 60)
    print("ENVIRONMENT VARIABLES CHECK")
    print("=" * 60)

    required_vars = [
        'WEEKLY_REPORT_ENABLED',
        'RESEND_API_KEY',
        'RESEND_FROM_EMAIL',
        'WEEKLY_REPORT_DAY',
        'WEEKLY_REPORT_HOUR',
        'WEEKLY_REPORT_TIMEZONE'
    ]

    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Hide sensitive data
            if 'API_KEY' in var:
                display_value = value[:10] + "..." if len(value) > 10 else "SET"
            else:
                display_value = value
            print(f"✓ {var}: {display_value}")
        else:
            print(f"✗ {var}: NOT SET")
            all_set = False

    print()
    return all_set


def check_workspace_members():
    """Check workspaces and their members"""
    print("=" * 60)
    print("WORKSPACE MEMBERS CHECK")
    print("=" * 60)

    db = SessionLocal()
    try:
        workspaces = db.query(Workspace).all()

        if not workspaces:
            print("✗ No workspaces found!")
            return False

        print(f"Found {len(workspaces)} workspace(s)\n")

        has_recipients = False
        for workspace in workspaces:
            print(f"Workspace: {workspace.name} (ID: {workspace.id})")

            members = db.query(WorkspaceMember, User).join(
                User, WorkspaceMember.user_id == User.id
            ).filter(
                WorkspaceMember.workspace_id == workspace.id
            ).all()

            if not members:
                print(f"  ✗ No members found")
            else:
                print(f"  Found {len(members)} member(s):")
                for member, user in members:
                    email_status = "✓" if user.email else "✗ NO EMAIL"
                    role_info = f"({user.role})" if hasattr(user, 'role') else "(no role)"
                    print(f"    {email_status} {user.full_name} - {user.email or 'N/A'} {role_info}")
                    if user.email:
                        has_recipients = True
            print()

        return has_recipients

    finally:
        db.close()


def check_scheduler_settings():
    """Check scheduler configuration"""
    print("=" * 60)
    print("SCHEDULER CONFIGURATION")
    print("=" * 60)

    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    enabled = os.getenv('WEEKLY_REPORT_ENABLED', 'True').lower() == 'true'
    day = int(os.getenv('WEEKLY_REPORT_DAY', '6'))
    hour = int(os.getenv('WEEKLY_REPORT_HOUR', '17'))
    timezone = os.getenv('WEEKLY_REPORT_TIMEZONE', 'Africa/Nairobi')

    print(f"Enabled: {enabled}")
    print(f"Schedule: Every {day_names[day]} at {hour:02d}:00 {timezone}")
    print()

    if not enabled:
        print("⚠ WARNING: Weekly reports are DISABLED")
        return False

    return True


def main():
    print("\n🔍 SCHEDULER DIAGNOSTIC CHECK\n")

    env_ok = check_environment()
    scheduler_ok = check_scheduler_settings()
    members_ok = check_workspace_members()

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    if env_ok and scheduler_ok and members_ok:
        print("✓ All checks passed! Scheduler should work correctly.")
        print("\n💡 If emails still aren't sending:")
        print("   1. Restart your FastAPI server")
        print("   2. Check server logs for 'Scheduler started' message")
        print("   3. Test manually: POST /api/field-activities/trigger-weekly-report")
    else:
        print("✗ Issues found:")
        if not env_ok:
            print("   - Missing required environment variables")
        if not scheduler_ok:
            print("   - Scheduler is disabled")
        if not members_ok:
            print("   - No workspace members with email addresses")

    print()


if __name__ == "__main__":
    main()
