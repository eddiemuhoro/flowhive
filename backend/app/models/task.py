from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    task_list_id = Column(Integer, ForeignKey("task_lists.id"), nullable=False)
    parent_task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)  # For subtasks
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)
    due_date = Column(DateTime, nullable=True)
    start_date = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    position = Column(Integer, default=0)
    estimated_hours = Column(Integer, nullable=True)
    actual_hours = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    task_list = relationship("TaskList", back_populates="tasks")
    creator = relationship("User", back_populates="created_tasks", foreign_keys=[creator_id])
    assignee = relationship("User", back_populates="assigned_tasks", foreign_keys=[assignee_id])
    parent_task = relationship("Task", remote_side=[id], backref="subtasks")
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
    attachments = relationship("Attachment", back_populates="task", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLog", back_populates="task", cascade="all, delete-orphan")
