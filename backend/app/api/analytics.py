from typing import List, Dict
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.database import get_db
from app.models.user import User, UserRole
from app.models.workspace import Workspace, WorkspaceMember
from app.models.project import Project, TaskList
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.analytics import (
    TaskAnalytics,
    ProjectAnalytics,
    UserProductivity,
    WorkspaceAnalytics,
    ExecutiveDashboard
)
from app.utils.auth import get_current_active_user, require_role

router = APIRouter()


def calculate_completion_rate(completed: int, total: int) -> float:
    """Calculate completion rate as percentage"""
    return round((completed / total * 100) if total > 0 else 0, 2)


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
        query = query.join(Task.task_list).join(TaskList.project).filter(
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
    tasks = db.query(Task).join(Task.task_list).filter(
        TaskList.project_id == project_id
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
            tasks_query = tasks_query.join(Task.task_list).join(TaskList.project).filter(
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

        workspace_tasks = db.query(Task).join(Task.task_list).join(TaskList.project).filter(
            Project.workspace_id == workspace.id
        )

        ws_total = workspace_tasks.count()
        ws_completed = workspace_tasks.filter(Task.status == TaskStatus.COMPLETED).count()

        active_members = db.query(WorkspaceMember).filter(
            WorkspaceMember.workspace_id == workspace.id
        ).count()

        project_analytics = []
        for project in projects:
            proj_tasks = db.query(Task).join(Task.task_list).filter(
                TaskList.project_id == project.id
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

        workspace_analytics.append(WorkspaceAnalytics(
            workspace_id=workspace.id,
            workspace_name=workspace.name,
            total_projects=len(projects),
            total_tasks=ws_total,
            completed_tasks=ws_completed,
            active_members=active_members,
            completion_rate=calculate_completion_rate(ws_completed, ws_total),
            projects=project_analytics
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
