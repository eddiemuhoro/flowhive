from typing import List, Optional
import os
import uuid
from datetime import date, datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Body
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import aiofiles
from app.database import get_db
from app.models.user import User, UserRole
from app.models.workspace import WorkspaceMember
from app.models.field_activity import FieldActivity, TaskCategory, FieldActivityPhoto, ActivityStatus
from app.schemas.field_activity import (
    FieldActivityCreate,
    FieldActivityUpdate,
    FieldActivityResponse,
    FieldActivityDetailResponse,
    FieldActivityPhotoResponse
)
from app.utils.auth import get_current_active_user, require_role
from app.utils.sanitizer import sanitize_html
from app.utils.email import send_activity_report_email
from app.config import settings

router = APIRouter()

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp", "image/heic"}


@router.post("/", response_model=FieldActivityResponse, status_code=status.HTTP_201_CREATED)
async def create_field_activity(
    activity_data: FieldActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new field activity"""
    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == activity_data.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Check if creating task for someone else (PENDING status)
    if activity_data.status == ActivityStatus.PENDING:
        # Only managers/executives can create pending tasks for others
        if activity_data.support_staff_id != current_user.id:
            if current_user.role not in [UserRole.MANAGER, UserRole.EXECUTIVE]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Only managers/executives can assign tasks to other staff"
                )

    # Validate task_category belongs to same workspace if provided
    if activity_data.task_category_id:
        category = db.query(TaskCategory).filter(TaskCategory.id == activity_data.task_category_id).first()
        if not category or category.workspace_id != activity_data.workspace_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task category for this workspace"
            )

    # Sanitize HTML content
    activity_dict = activity_data.model_dump()
    if activity_dict.get('task_description'):
        activity_dict['task_description'] = sanitize_html(activity_dict['task_description'])
    if activity_dict.get('remarks'):
        activity_dict['remarks'] = sanitize_html(activity_dict['remarks'])

    activity = FieldActivity(
        **activity_dict,
        created_by=current_user.id
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)

    # Populate computed fields for response
    activity.support_staff_name = activity.support_staff.full_name or activity.support_staff.username
    activity.created_by_name = current_user.full_name or current_user.username

    return activity


@router.get("/workspace/{workspace_id}", response_model=List[FieldActivityResponse])
async def get_workspace_field_activities(
    workspace_id: int,
    date_from: Optional[date] = Query(None, description="Filter from date"),
    date_to: Optional[date] = Query(None, description="Filter to date"),
    support_staff_id: Optional[int] = Query(None, description="Filter by staff member"),
    task_category_id: Optional[int] = Query(None, description="Filter by category"),
    customer_name: Optional[str] = Query(None, description="Search customer name"),
    search: Optional[str] = Query(None, description="Search in task description"),
    status: Optional[ActivityStatus] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all field activities for a workspace with optional filters"""
    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Build query with filters
    query = db.query(FieldActivity).filter(FieldActivity.workspace_id == workspace_id)

    if date_from:
        query = query.filter(FieldActivity.activity_date >= date_from)

    if date_to:
        query = query.filter(FieldActivity.activity_date <= date_to)

    if support_staff_id:
        query = query.filter(FieldActivity.support_staff_id == support_staff_id)

    if task_category_id:
        query = query.filter(FieldActivity.task_category_id == task_category_id)

    if customer_name:
        query = query.filter(FieldActivity.customer_name.ilike(f"%{customer_name}%"))

    if search:
        query = query.filter(FieldActivity.task_description.ilike(f"%{search}%"))

    if status:
        query = query.filter(FieldActivity.status == status)

    activities = query.order_by(FieldActivity.activity_date.desc(), FieldActivity.start_time.desc()).all()

    # Filter activities based on user role and category required_role
    # Role hierarchy: team_member < manager < executive
    role_hierarchy = {"team_member": 0, "manager": 1, "executive": 2}
    user_role_level = role_hierarchy.get(current_user.role, 0)

    filtered_activities = []
    for activity in activities:
        # If activity has no category, show it to everyone
        if not activity.task_category_id:
            filtered_activities.append(activity)
        else:
            # Check if user's role meets the category's required role
            category = activity.task_category
            category_required_level = role_hierarchy.get(category.required_role, 0)
            if user_role_level >= category_required_level:
                filtered_activities.append(activity)

    # Populate computed fields
    for activity in filtered_activities:
        activity.support_staff_name = activity.support_staff.full_name or activity.support_staff.username
        activity.created_by_name = activity.created_by_user.full_name or activity.created_by_user.username
        if activity.updated_by:
            activity.updated_by_name = activity.updated_by_user.full_name or activity.updated_by_user.username

    return filtered_activities


@router.get("/{activity_id}", response_model=FieldActivityDetailResponse)
async def get_field_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific field activity with photos"""
    activity = db.query(FieldActivity).filter(FieldActivity.id == activity_id).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field activity not found"
        )

    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == activity.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Check if user has permission to view this activity based on category role
    if activity.task_category_id:
        category = activity.task_category
        role_hierarchy = {"team_member": 0, "manager": 1, "executive": 2}
        user_role_level = role_hierarchy.get(current_user.role, 0)
        category_required_level = role_hierarchy.get(category.required_role, 0)

        if user_role_level < category_required_level:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions to view this activity"
            )

    # Populate computed fields
    activity.support_staff_name = activity.support_staff.full_name or activity.support_staff.username
    activity.created_by_name = activity.created_by_user.full_name or activity.created_by_user.username
    if activity.updated_by:
        activity.updated_by_name = activity.updated_by_user.full_name or activity.updated_by_user.username

    return activity


@router.put("/{activity_id}", response_model=FieldActivityResponse)
async def update_field_activity(
    activity_id: int,
    activity_data: FieldActivityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update a field activity"""
    activity = db.query(FieldActivity).filter(FieldActivity.id == activity_id).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field activity not found"
        )

    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == activity.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Validate task_category if being updated
    if activity_data.task_category_id:
        category = db.query(TaskCategory).filter(TaskCategory.id == activity_data.task_category_id).first()
        if not category or category.workspace_id != activity.workspace_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task category for this workspace"
            )

    # Validate status transitions and required fields
    update_data = activity_data.model_dump(exclude_unset=True)

    # If updating to COMPLETED, ensure required fields are provided
    if 'status' in update_data and update_data['status'] == ActivityStatus.COMPLETED:
        # Check current activity state and updated data
        start_time = update_data.get('start_time') or activity.start_time
        end_time = update_data.get('end_time') or activity.end_time
        task_description = update_data.get('task_description') or activity.task_description

        if not start_time or not end_time or not task_description:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_time, end_time, and task_description are required when completing a task"
            )

    # Permission check: staff can only complete their own pending tasks
    if 'status' in update_data:
        if activity.support_staff_id != current_user.id:
            # Only managers/executives can update others' tasks
            if current_user.role not in [UserRole.MANAGER, UserRole.EXECUTIVE]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only update your own assigned tasks"
                )

    # Update activity fields

    # Sanitize HTML content if present
    if 'task_description' in update_data and update_data['task_description']:
        update_data['task_description'] = sanitize_html(update_data['task_description'])
    if 'remarks' in update_data and update_data['remarks']:
        update_data['remarks'] = sanitize_html(update_data['remarks'])

    for field, value in update_data.items():
        setattr(activity, field, value)

    activity.updated_by = current_user.id
    db.commit()
    db.refresh(activity)

    # Populate computed fields
    activity.support_staff_name = activity.support_staff.full_name or activity.support_staff.username
    activity.created_by_name = activity.created_by_user.full_name or activity.created_by_user.username
    activity.updated_by_name = current_user.full_name or current_user.username

    return activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_field_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a field activity"""
    activity = db.query(FieldActivity).filter(FieldActivity.id == activity_id).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field activity not found"
        )

    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == activity.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Only allow deletion by creator or managers/executives
    if activity.created_by != current_user.id and current_user.role == UserRole.TEAM_MEMBER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the creator or managers can delete this activity"
        )

    db.delete(activity)
    db.commit()

    return None


@router.get("/workspace/{workspace_id}/pending", response_model=List[FieldActivityResponse])
async def get_pending_tasks(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get pending tasks assigned to the current user"""
    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Get pending tasks assigned to current user
    pending_tasks = db.query(FieldActivity).filter(
        FieldActivity.workspace_id == workspace_id,
        FieldActivity.support_staff_id == current_user.id,
        FieldActivity.status == ActivityStatus.PENDING
    ).order_by(FieldActivity.activity_date.asc()).all()

    # Populate computed fields
    for task in pending_tasks:
        task.support_staff_name = task.support_staff.full_name or task.support_staff.username
        task.created_by_name = task.created_by_user.full_name or task.created_by_user.username
        if task.updated_by:
            task.updated_by_name = task.updated_by_user.full_name or task.updated_by_user.username

    return pending_tasks


@router.get("/workspace/{workspace_id}/assigned-by-me", response_model=List[FieldActivityResponse])
async def get_tasks_assigned_by_me(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.EXECUTIVE]))
):
    """Get pending tasks created by the current user (managers/executives only)"""
    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Get pending tasks created by current user
    assigned_tasks = db.query(FieldActivity).filter(
        FieldActivity.workspace_id == workspace_id,
        FieldActivity.created_by == current_user.id,
        FieldActivity.status == ActivityStatus.PENDING
    ).order_by(FieldActivity.activity_date.asc()).all()

    # Populate computed fields
    for task in assigned_tasks:
        task.support_staff_name = task.support_staff.full_name or task.support_staff.username
        task.created_by_name = task.created_by_user.full_name or task.created_by_user.username
        if task.updated_by:
            task.updated_by_name = task.updated_by_user.full_name or task.updated_by_user.username

    return assigned_tasks


@router.get("/workspace/{workspace_id}/analytics")
async def get_field_activity_analytics(
    workspace_id: int,
    date_from: Optional[date] = Query(None, description="Analytics from date"),
    date_to: Optional[date] = Query(None, description="Analytics to date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.MANAGER, UserRole.EXECUTIVE]))
):
    """Get analytics for field activities (managers/executives only)"""
    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Build base query
    query = db.query(FieldActivity).filter(FieldActivity.workspace_id == workspace_id)

    if date_from:
        query = query.filter(FieldActivity.activity_date >= date_from)
    if date_to:
        query = query.filter(FieldActivity.activity_date <= date_to)

    # Hours by staff member
    hours_by_staff = db.query(
        User.id,
        User.full_name,
        User.username,
        func.count(FieldActivity.id).label('activity_count')
    ).join(FieldActivity, FieldActivity.support_staff_id == User.id)\
     .filter(FieldActivity.workspace_id == workspace_id)

    if date_from:
        hours_by_staff = hours_by_staff.filter(FieldActivity.activity_date >= date_from)
    if date_to:
        hours_by_staff = hours_by_staff.filter(FieldActivity.activity_date <= date_to)

    hours_by_staff = hours_by_staff.group_by(User.id, User.full_name, User.username).all()

    # Activities by category
    activities_by_category = db.query(
        TaskCategory.title,
        func.count(FieldActivity.id).label('count')
    ).join(FieldActivity, FieldActivity.task_category_id == TaskCategory.id)\
     .filter(FieldActivity.workspace_id == workspace_id)

    if date_from:
        activities_by_category = activities_by_category.filter(FieldActivity.activity_date >= date_from)
    if date_to:
        activities_by_category = activities_by_category.filter(FieldActivity.activity_date <= date_to)

    activities_by_category = activities_by_category.group_by(TaskCategory.title).all()

    # Total activities
    total_activities = query.count()

    return {
        "total_activities": total_activities,
        "hours_by_staff": [
            {
                "user_id": row.id,
                "name": row.full_name or row.username,
                "activity_count": row.activity_count
            }
            for row in hours_by_staff
        ],
        "activities_by_category": [
            {
                "category": row.title,
                "count": row.count
            }
            for row in activities_by_category
        ]
    }


@router.post("/{activity_id}/photos", response_model=FieldActivityPhotoResponse, status_code=status.HTTP_201_CREATED)
async def upload_field_activity_photo(
    activity_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload a photo for a field activity"""
    # Get activity
    activity = db.query(FieldActivity).filter(FieldActivity.id == activity_id).first()

    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Field activity not found"
        )

    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == activity.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Validate file size
    file_content = await file.read()
    file_size = len(file_content)

    max_size = 10 * 1024 * 1024  # 10MB
    if file_size > max_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {max_size} bytes"
        )

    # Validate file type
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file.content_type} not allowed. Only images are supported."
        )

    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join("uploads", "field_photos", unique_filename)

    # Ensure directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(file_content)

    # Create photo record
    photo = FieldActivityPhoto(
        field_activity_id=activity_id,
        file_path=file_path,
        file_name=file.filename,
        file_size=file_size,
        mime_type=file.content_type,
        uploaded_by=current_user.id
    )

    db.add(photo)
    db.commit()
    db.refresh(photo)

    return photo


@router.delete("/{activity_id}/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_field_activity_photo(
    activity_id: int,
    photo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a photo from a field activity"""
    # Get photo
    photo = db.query(FieldActivityPhoto).filter(
        FieldActivityPhoto.id == photo_id,
        FieldActivityPhoto.field_activity_id == activity_id
    ).first()

    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Photo not found"
        )

    # Get activity
    activity = db.query(FieldActivity).filter(FieldActivity.id == activity_id).first()

    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == activity.workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Delete file from filesystem
    if os.path.exists(photo.file_path):
        os.remove(photo.file_path)

    # Delete photo record
    db.delete(photo)
    db.commit()

    return None


@router.post("/workspace/{workspace_id}/send-report")
async def send_activity_report(
    workspace_id: int,
    date_from: str = Body(...),
    date_to: str = Body(...),
    recipient_emails: List[str] = Body(...),
    support_staff_id: Optional[int] = Body(None),
    send_individual_reports: bool = Body(False, description="Send personalized reports to each staff member"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Send activity report via email

    If send_individual_reports=True:
    - Each staff member receives only their own activities
    - Managers/Executives in recipient list receive full report

    If send_individual_reports=False (default):
    - All recipients receive the same full report
    """
    # Check if user is workspace member
    is_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not a member of this workspace"
        )

    # Build query
    query = db.query(FieldActivity).filter(
        FieldActivity.workspace_id == workspace_id
    )

    # Apply filters
    if date_from:
        query = query.filter(FieldActivity.activity_date >= date_from)
    if date_to:
        query = query.filter(FieldActivity.activity_date <= date_to)
    if support_staff_id:
        query = query.filter(FieldActivity.support_staff_id == support_staff_id)

    # Get activities
    activities = query.order_by(
        FieldActivity.activity_date,
        FieldActivity.start_time
    ).all()

    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activities found for the specified criteria"
        )

    if send_individual_reports:
        # Send personalized reports to each workspace member
        return await _send_individual_reports(
            workspace_id, activities, date_from, date_to, db
        )
    else:
        # Send same report to all recipients (original behavior)
        return await _send_bulk_report(
            activities, recipient_emails, date_from, date_to
        )


async def _send_bulk_report(
    activities: List[FieldActivity],
    recipient_emails: List[str],
    date_from: str,
    date_to: str
):
    """Send the same full report to all specified recipients"""
    # Group activities by staff
    activities_by_staff = {}
    for activity in activities:
        staff_id = activity.support_staff_id
        if staff_id not in activities_by_staff:
            activities_by_staff[staff_id] = {
                'staff_name': activity.support_staff.full_name or activity.support_staff.username,
                'activities': [],
                'total_hours': 0
            }

        # Convert activity to dict
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

        activities_by_staff[staff_id]['activities'].append(activity_dict)
        activities_by_staff[staff_id]['total_hours'] += activity.duration_hours or 0

    # Convert to list
    activities_list = list(activities_by_staff.values())

    # Calculate summary
    total_hours = sum(a.duration_hours or 0 for a in activities)
    unique_customers = len(set(a.customer_name for a in activities))
    unique_staff = len(activities_by_staff)

    summary = {
        'total_activities': len(activities),
        'total_hours': total_hours,
        'unique_customers': unique_customers,
        'unique_staff': unique_staff
    }

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
        resend_api_key=settings.RESEND_API_KEY,
        from_email=settings.RESEND_FROM_EMAIL,
        from_name=settings.RESEND_FROM_NAME,
        frontend_url=settings.FRONTEND_URL
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


async def _send_individual_reports(
    workspace_id: int,
    activities: List[FieldActivity],
    date_from: str,
    date_to: str,
    db: Session
):
    """
    Send personalized reports to each staff member
    - Team members get only their activities
    - Managers/Executives get full reports
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
                resend_api_key=settings.RESEND_API_KEY,
                from_email=settings.RESEND_FROM_EMAIL,
                from_name=settings.RESEND_FROM_NAME,
                frontend_url=settings.FRONTEND_URL
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


@router.post("/trigger-weekly-report")
async def trigger_weekly_report_manually(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.EXECUTIVE]))
):
    """
    Manually trigger the weekly report job (Executives only)
    Useful for testing the automated email system
    """
    from app.scheduler import send_weekly_reports

    try:
        await send_weekly_reports()
        return {
            'message': 'Weekly report job triggered successfully',
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'Failed to trigger weekly report: {str(e)}'
        )
