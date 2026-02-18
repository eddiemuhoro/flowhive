from typing import List, Dict
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.database import get_db
from app.models.user import User, UserRole
from app.models.workspace import Workspace, WorkspaceMember
from app.models.project import Project
from app.models.task import Task, TaskStatus, TaskPriority
from app.models.field_activity import FieldActivity, TaskCategory, LocationType
from app.schemas.analytics import (
    TaskAnalytics,
    ProjectAnalytics,
    UserProductivity,
    WorkspaceAnalytics,
    ExecutiveDashboard,
    FieldActivityAnalytics
)
from app.utils.auth import get_current_active_user, require_role

router = APIRouter()


def calculate_completion_rate(completed: int, total: int) -> float:
    """Calculate completion rate as percentage"""
    return round((completed / total * 100) if total > 0 else 0, 2)


def get_field_activity_analytics(db: Session, workspace_id: int) -> FieldActivityAnalytics:
    """Get field activity analytics for a workspace"""
    activities = db.query(FieldActivity).filter(
        FieldActivity.workspace_id == workspace_id
    )

    total_activities = activities.count()

    # Calculate total hours
    all_activities = activities.all()
    total_hours = sum([activity.duration_hours for activity in all_activities])

    # Activities this week
    now = datetime.utcnow()
    week_start = now - timedelta(days=now.weekday())
    activities_this_week = activities.filter(
        FieldActivity.activity_date >= week_start.date()
    ).count()

    # Activities this month
    month_start = now.replace(day=1)
    activities_this_month = activities.filter(
        FieldActivity.activity_date >= month_start.date()
    ).count()

    # Top staff by activity count
    staff_stats = db.query(
        User.id,
        User.full_name,
        User.username,
        func.count(FieldActivity.id).label('activity_count')
    ).join(
        FieldActivity, FieldActivity.support_staff_id == User.id
    ).filter(
        FieldActivity.workspace_id == workspace_id
    ).group_by(User.id, User.full_name, User.username).order_by(
        func.count(FieldActivity.id).desc()
    ).limit(5).all()

    top_staff = [
        {
            "user_id": user_id,
            "name": full_name or username,
            "activity_count": count
        }
        for user_id, full_name, username, count in staff_stats
    ]

    # Category distribution
    category_stats = db.query(
        TaskCategory.title,
        func.count(FieldActivity.id).label('count')
    ).join(
        FieldActivity, FieldActivity.task_category_id == TaskCategory.id
    ).filter(
        FieldActivity.workspace_id == workspace_id
    ).group_by(TaskCategory.title).all()

    category_distribution = {title: count for title, count in category_stats}

    # Add uncategorized activities
    uncategorized = activities.filter(FieldActivity.task_category_id.is_(None)).count()
    if uncategorized > 0:
        category_distribution["Uncategorized"] = uncategorized

    # Top customers by visit count
    top_customers_stats = db.query(
        FieldActivity.customer_name,
        func.count(FieldActivity.id).label('visit_count')
    ).filter(
        FieldActivity.workspace_id == workspace_id,
        FieldActivity.customer_name.isnot(None)
    ).group_by(
        FieldActivity.customer_name
    ).order_by(
        func.count(FieldActivity.id).desc()
    ).limit(6).all()

    top_customers = [
        {
            "customer_name": name,
            "visit_count": count
        }
        for name, count in top_customers_stats
    ]

    # Unique customers served
    unique_customers = db.query(
        func.count(func.distinct(FieldActivity.customer_id))
    ).filter(
        FieldActivity.workspace_id == workspace_id,
        FieldActivity.customer_id.isnot(None)
    ).scalar() or 0

    # Billing metrics (ON_SITE vs OFFICE)
    billable_hours = 0.0
    non_billable_hours = 0.0
    billable_visits = 0
    office_activities = 0

    for activity in all_activities:
        hours = activity.duration_hours
        if activity.location_type == LocationType.ON_SITE:
            billable_hours += hours
            billable_visits += 1
        else:  # OFFICE
            non_billable_hours += hours
            office_activities += 1

    # Calculate billing rate percentage
    billing_rate = (billable_hours / total_hours * 100) if total_hours > 0 else 0.0

    return FieldActivityAnalytics(
        total_activities=total_activities,
        total_hours=round(total_hours, 2),
        activities_this_week=activities_this_week,
        activities_this_month=activities_this_month,
        top_staff=top_staff,
        category_distribution=category_distribution,
        top_customers=top_customers,
        unique_customers=unique_customers,
        billable_hours=round(billable_hours, 2),
        non_billable_hours=round(non_billable_hours, 2),
        billable_visits=billable_visits,
        office_activities=office_activities,
        billing_rate=round(billing_rate, 1)
    )


@router.get("/field-activities/overview", response_model=FieldActivityAnalytics)
async def get_field_activity_analytics_endpoint(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get field activity analytics for a workspace"""
    return get_field_activity_analytics(db, workspace_id)


@router.get("/customers/top-customers", response_model=List[Dict])
async def get_top_customers(
    workspace_id: int,
    limit: int = 10,
    date_from: datetime = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get top customers by activity count"""
    query = db.query(
        FieldActivity.customer_id,
        FieldActivity.customer_name,
    ).filter(
        FieldActivity.workspace_id == workspace_id,
        FieldActivity.customer_id.isnot(None)
    )

    if date_from:
        query = query.filter(FieldActivity.activity_date >= date_from.date())

    # Get all activities grouped by customer
    activities = query.all()

    # Group by customer and calculate stats
    customer_stats = {}
    for activity in db.query(FieldActivity).filter(
        FieldActivity.workspace_id == workspace_id,
        FieldActivity.customer_id.isnot(None)
    ).all():
        if date_from and activity.activity_date < date_from.date():
            continue

        cust_id = activity.customer_id
        if cust_id not in customer_stats:
            customer_stats[cust_id] = {
                "customer_id": cust_id,
                "customer_name": activity.customer_name,
                "activity_count": 0,
                "total_hours": 0.0
            }
        customer_stats[cust_id]["activity_count"] += 1
        customer_stats[cust_id]["total_hours"] += activity.duration_hours

    # Sort by activity count and limit
    result = sorted(
        customer_stats.values(),
        key=lambda x: x['activity_count'],
        reverse=True
    )[:limit]

    # Round hours
    for item in result:
        item["total_hours"] = round(item["total_hours"], 2)

    return result


@router.get("/customers/{customer_id}/timeline", response_model=Dict)
async def get_customer_timeline(
    customer_id: str,
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get activity timeline for a specific customer"""
    activities = db.query(FieldActivity).filter(
        FieldActivity.workspace_id == workspace_id,
        FieldActivity.customer_id == customer_id
    ).order_by(FieldActivity.activity_date.desc()).all()

    if not activities:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No activities found for this customer"
        )

    return {
        "customer_id": customer_id,
        "customer_name": activities[0].customer_name,
        "last_visit": activities[0].activity_date.isoformat(),
        "first_visit": activities[-1].activity_date.isoformat(),
        "total_visits": len(activities),
        "total_hours": round(sum(a.duration_hours for a in activities), 2),
        "recent_activities": [
            {
                "id": a.id,
                "date": a.activity_date.isoformat(),
                "title": a.title,
                "category": a.task_category.title if a.task_category else None,
                "hours": round(a.duration_hours, 2),
                "status": a.status.value
            }
            for a in activities[:5]  # Last 5 activities
        ]
    }


@router.get("/customers/health-check", response_model=List[Dict])
async def get_customer_health_check(
    workspace_id: int,
    days_threshold: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Identify customers at risk (not visited recently)"""

    # Get last visit date per customer
    subquery = db.query(
        FieldActivity.customer_id,
        FieldActivity.customer_name,
        func.max(FieldActivity.activity_date).label('last_visit'),
        func.count(FieldActivity.id).label('total_visits')
    ).filter(
        FieldActivity.workspace_id == workspace_id,
        FieldActivity.customer_id.isnot(None)
    ).group_by(
        FieldActivity.customer_id,
        FieldActivity.customer_name
    ).subquery()

    results = db.query(subquery).all()

    now = datetime.utcnow().date()
    customer_health = []

    for customer in results:
        days_since_visit = (now - customer.last_visit).days
        status_value = "healthy" if days_since_visit < days_threshold else "at_risk"

        customer_health.append({
            "customer_id": customer.customer_id,
            "customer_name": customer.customer_name,
            "last_visit": customer.last_visit.isoformat(),
            "days_since_visit": days_since_visit,
            "total_visits": customer.total_visits,
            "status": status_value
        })

    # Sort by days since visit (descending)
    customer_health.sort(key=lambda x: x['days_since_visit'], reverse=True)
    return customer_health


@router.get("/customers/visit-frequency", response_model=List[Dict])
async def get_customer_visit_frequency(
    workspace_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Calculate average days between visits per customer"""
    customers = db.query(
        FieldActivity.customer_id,
        FieldActivity.customer_name
    ).filter(
        FieldActivity.workspace_id == workspace_id,
        FieldActivity.customer_id.isnot(None)
    ).distinct().all()

    frequency_data = []

    for cust_id, cust_name in customers:
        visits = db.query(FieldActivity.activity_date).filter(
            FieldActivity.workspace_id == workspace_id,
            FieldActivity.customer_id == cust_id
        ).order_by(FieldActivity.activity_date).all()

        if len(visits) < 2:
            continue

        # Calculate gaps between visits
        gaps = [
            (visits[i+1][0] - visits[i][0]).days
            for i in range(len(visits) - 1)
        ]

        avg_gap = sum(gaps) / len(gaps) if gaps else 0

        frequency_data.append({
            "customer_id": cust_id,
            "customer_name": cust_name,
            "total_visits": len(visits),
            "avg_days_between_visits": round(avg_gap, 1),
            "frequency_category": (
                "weekly" if avg_gap <= 7 else
                "biweekly" if avg_gap <= 14 else
                "monthly" if avg_gap <= 31 else
                "quarterly" if avg_gap <= 90 else
                "infrequent"
            )
        })

    return sorted(frequency_data, key=lambda x: x['avg_days_between_visits'])


@router.get("/overview", response_model=TaskAnalytics)
async def get_task_analytics(
    workspace_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get overall task analytics"""
    query = db.query(Task)

    # Filter by workspace if provided
    if workspace_id:
        query = query.join(Task.project).filter(
            Project.workspace_id == workspace_id
        )

    total_tasks = query.count()
    completed_tasks = query.filter(Task.status == TaskStatus.COMPLETED).count()
    in_progress_tasks = query.filter(Task.status == TaskStatus.IN_PROGRESS).count()

    # Overdue tasks
    now = datetime.utcnow()
    overdue_tasks = query.filter(
        Task.due_date < now,
        Task.status != TaskStatus.COMPLETED
    ).count()

    # Average completion time
    completed_with_dates = query.filter(
        Task.status == TaskStatus.COMPLETED,
        Task.completed_at.isnot(None),
        Task.created_at.isnot(None)
    ).all()

    avg_completion_time = None
    if completed_with_dates:
        total_days = sum([
            (task.completed_at - task.created_at).days
            for task in completed_with_dates
        ])
        avg_completion_time = round(total_days / len(completed_with_dates), 2)

    return TaskAnalytics(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        in_progress_tasks=in_progress_tasks,
        overdue_tasks=overdue_tasks,
        completion_rate=calculate_completion_rate(completed_tasks, total_tasks),
        average_completion_time=avg_completion_time
    )


@router.get("/projects/{project_id}", response_model=ProjectAnalytics)
async def get_project_analytics(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get analytics for a specific project"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )

    # Get tasks in this project
    tasks = db.query(Task).filter(
        Task.project_id == project_id
    )

    total_tasks = tasks.count()
    completed_tasks = tasks.filter(Task.status == TaskStatus.COMPLETED).count()

    return ProjectAnalytics(
        project_id=project.id,
        project_name=project.name,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        completion_rate=calculate_completion_rate(completed_tasks, total_tasks)
    )


@router.get("/user-productivity", response_model=List[UserProductivity])
async def get_user_productivity(
    workspace_id: int = None,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user productivity metrics"""
    #check is user is in the workspace if workspace_id is provided
    if workspace_id:
        membership = db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == workspace_id,
            WorkspaceMember.user_id == current_user.id
        ).first()
        if not membership:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not a member of this workspace"
            )

    if current_user.role not in [UserRole.MANAGER, UserRole.EXECUTIVE]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    # Get workspace members
    users_query = db.query(User)
    if workspace_id:
        users_query = users_query.join(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == workspace_id
        )

    users = users_query.all()
    productivity_data = []

    for user in users:
        tasks_query = db.query(Task).filter(Task.assignee_id == user.id)

        if workspace_id:
            tasks_query = tasks_query.join(Task.project).filter(
                Project.workspace_id == workspace_id
            )

        tasks_assigned = tasks_query.count()
        tasks_completed = tasks_query.filter(Task.status == TaskStatus.COMPLETED).count()

        # Calculate average hours per task
        completed_with_hours = tasks_query.filter(
            Task.status == TaskStatus.COMPLETED,
            Task.actual_hours.isnot(None)
        ).all()

        avg_hours = None
        if completed_with_hours:
            total_hours = sum([task.actual_hours for task in completed_with_hours])
            avg_hours = round(total_hours / len(completed_with_hours), 2)

        productivity_data.append(UserProductivity(
            user_id=user.id,
            user_name=user.full_name or user.username,
            tasks_assigned=tasks_assigned,
            tasks_completed=tasks_completed,
            completion_rate=calculate_completion_rate(tasks_completed, tasks_assigned),
            average_hours_per_task=avg_hours
        ))

    # Sort by completion rate
    productivity_data.sort(key=lambda x: x.completion_rate, reverse=True)
    return productivity_data[:limit]


@router.get("/executive-dashboard", response_model=ExecutiveDashboard)
async def get_executive_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.EXECUTIVE]))
):
    """Get executive dashboard with comprehensive analytics"""
    # Overall task analytics
    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == TaskStatus.COMPLETED).count()
    in_progress_tasks = db.query(Task).filter(Task.status == TaskStatus.IN_PROGRESS).count()

    now = datetime.utcnow()
    overdue_tasks = db.query(Task).filter(
        Task.due_date < now,
        Task.status != TaskStatus.COMPLETED
    ).count()

    overview = TaskAnalytics(
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        in_progress_tasks=in_progress_tasks,
        overdue_tasks=overdue_tasks,
        completion_rate=calculate_completion_rate(completed_tasks, total_tasks),
        average_completion_time=None
    )

    # Workspace analytics
    workspaces = db.query(Workspace).all()
    workspace_analytics = []

    for workspace in workspaces:
        projects = db.query(Project).filter(Project.workspace_id == workspace.id).all()

        workspace_tasks = db.query(Task).join(Task.project).filter(
            Project.workspace_id == workspace.id
        )

        ws_total = workspace_tasks.count()
        ws_completed = workspace_tasks.filter(Task.status == TaskStatus.COMPLETED).count()

        active_members = db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == workspace.id
        ).count()

        project_analytics = []
        for project in projects:
            proj_tasks = db.query(Task).filter(
                Task.project_id == project.id
            )
            proj_total = proj_tasks.count()
            proj_completed = proj_tasks.filter(Task.status == TaskStatus.COMPLETED).count()

            project_analytics.append(ProjectAnalytics(
                project_id=project.id,
                project_name=project.name,
                total_tasks=proj_total,
                completed_tasks=proj_completed,
                completion_rate=calculate_completion_rate(proj_completed, proj_total)
            ))

        # Include field activities for this workspace
        field_activity_count = db.query(FieldActivity).filter(
            FieldActivity.workspace_id == workspace.id
        ).count()

        field_analytics = None
        if field_activity_count > 0:
            field_analytics = get_field_activity_analytics(db, workspace.id)

        workspace_analytics.append(WorkspaceAnalytics(
            workspace_id=workspace.id,
            workspace_name=workspace.name,
            total_projects=len(projects),
            total_tasks=ws_total,
            completed_tasks=ws_completed,
            active_members=active_members,
            completion_rate=calculate_completion_rate(ws_completed, ws_total),
            projects=project_analytics,
            field_activities=field_analytics
        ))

    # Top performers (top 5)
    users = db.query(User).all()
    user_productivity = []

    for user in users:
        tasks_assigned = db.query(Task).filter(Task.assignee_id == user.id).count()
        tasks_completed = db.query(Task).filter(
            Task.assignee_id == user.id,
            Task.status == TaskStatus.COMPLETED
        ).count()

        if tasks_assigned > 0:
            user_productivity.append(UserProductivity(
                user_id=user.id,
                user_name=user.full_name or user.username,
                tasks_assigned=tasks_assigned,
                tasks_completed=tasks_completed,
                completion_rate=calculate_completion_rate(tasks_completed, tasks_assigned),
                average_hours_per_task=None
            ))

    user_productivity.sort(key=lambda x: x.completion_rate, reverse=True)
    top_performers = user_productivity[:5]

    # Task completion trend (last 7 days)
    completion_trend = []
    for i in range(6, -1, -1):
        date = now - timedelta(days=i)
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)

        completed_on_day = db.query(Task).filter(
            Task.completed_at >= day_start,
            Task.completed_at < day_end
        ).count()

        completion_trend.append({
            "date": day_start.strftime("%Y-%m-%d"),
            "completed": completed_on_day
        })

    # Priority distribution
    priority_dist = {}
    for priority in TaskPriority:
        count = db.query(Task).filter(Task.priority == priority).count()
        priority_dist[priority.value] = count

    # Status distribution
    status_dist = {}
    for status_enum in TaskStatus:
        count = db.query(Task).filter(Task.status == status_enum).count()
        status_dist[status_enum.value] = count

    return ExecutiveDashboard(
        overview=overview,
        workspaces=workspace_analytics,
        top_performers=top_performers,
        task_completion_trend=completion_trend,
        priority_distribution=priority_dist,
        status_distribution=status_dist
    )
