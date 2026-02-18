from datetime import datetime, time, timedelta
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date, Time, Boolean, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum


class ActivityStatus(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"


class LocationType(str, enum.Enum):
    OFFICE = "OFFICE"  # Work done from office/remotely
    ON_SITE = "ON_SITE"  # Physical visit to customer location


class TaskCategory(Base):
    __tablename__ = "task_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Internal identifier/slug
    title = Column(String, nullable=False)  # Display name shown to users
    description = Column(Text, nullable=True)  # Long text describing all tasks done
    color = Column(String, nullable=True)  # Hex color for UI display
    icon = Column(String, nullable=True)  # Icon name/emoji for UI
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False, index=True)
    required_role = Column(String, nullable=False, default="team_member")  # Minimum role required to view activities with this category
    is_active = Column(Boolean, default=True)  # Soft delete
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # User who created the category
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    workspace = relationship("Workspace", backref="task_categories")
    created_by_user = relationship("User", foreign_keys=[created_by])
    field_activities = relationship("FieldActivity", back_populates="task_category")


class FieldActivity(Base):
    __tablename__ = "field_activities"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    support_staff_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    activity_date = Column(Date, nullable=False, index=True)
    start_time = Column(Time, nullable=True)  # Nullable for pending tasks
    end_time = Column(Time, nullable=True)  # Nullable for pending tasks
    title = Column(String, nullable=False)  # Short summary of activity
    customer_id = Column(String, nullable=True)  # External customer ID from SAJSoft
    customer_name = Column(String, nullable=False)
    location_type = Column(Enum(LocationType), nullable=False, default=LocationType.ON_SITE, index=True)  # Work location type
    location = Column(String, nullable=False)
    task_category_id = Column(Integer, ForeignKey("task_categories.id"), nullable=True, index=True)
    task_description = Column(Text, nullable=True)  # Nullable for pending tasks
    remarks = Column(Text, nullable=True)
    customer_rep = Column(String, nullable=True)
    status = Column(Enum(ActivityStatus), nullable=False, default=ActivityStatus.COMPLETED, index=True)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    workspace = relationship("Workspace", back_populates="field_activities")
    support_staff = relationship("User", foreign_keys=[support_staff_id], backref="assigned_field_activities")
    created_by_user = relationship("User", foreign_keys=[created_by], backref="created_field_activities")
    updated_by_user = relationship("User", foreign_keys=[updated_by], backref="updated_field_activities")
    task_category = relationship("TaskCategory", back_populates="field_activities")
    photos = relationship("FieldActivityPhoto", back_populates="field_activity", cascade="all, delete-orphan")

    @property
    def duration_hours(self) -> float:
        """Calculate duration in hours between start_time and end_time"""
        if self.start_time and self.end_time:
            # Convert time objects to datetime for calculation
            start_dt = datetime.combine(datetime.today(), self.start_time)
            end_dt = datetime.combine(datetime.today(), self.end_time)

            # Handle overnight shifts (end time is next day)
            if end_dt < start_dt:
                end_dt = datetime.combine(datetime.today(), self.end_time) + timedelta(days=1)

            duration = end_dt - start_dt
            return round(duration.total_seconds() / 3600, 2)  # Convert to hours with 2 decimal places
        return 0.0


class FieldActivityPhoto(Base):
    __tablename__ = "field_activity_photos"

    id = Column(Integer, primary_key=True, index=True)
    field_activity_id = Column(Integer, ForeignKey("field_activities.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String, nullable=False)
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    field_activity = relationship("FieldActivity", back_populates="photos")
    uploaded_by_user = relationship("User", backref="uploaded_field_photos")
