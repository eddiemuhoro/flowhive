"""
Meeting Minutes Models
Models for meeting minutes and attachments in field operations
"""
from sqlalchemy import Column, Integer, String, Text, Date, Time, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class MeetingMinute(Base):
    """Model for meeting minutes in field operations"""
    __tablename__ = "meeting_minutes"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False, index=True)
    meeting_date = Column(Date, nullable=False, index=True)
    meeting_time_start = Column(Time, nullable=True)
    meeting_time_end = Column(Time, nullable=True)
    location = Column(String, nullable=True)
    
    # Attendees stored as JSON array of user IDs or names
    attendees = Column(JSON, nullable=True)  # e.g., [{"id": 1, "name": "John Doe"}, ...]
    
    # Meeting content (rich text)
    agenda = Column(Text, nullable=True)  # HTML/Rich text
    discussions = Column(Text, nullable=True)  # HTML/Rich text - main content
    decisions = Column(Text, nullable=True)  # HTML/Rich text
    
    # Metadata
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    updated_at = Column(DateTime, nullable=True, onupdate=datetime.utcnow)

    # Relationships
    workspace = relationship("Workspace", backref="meeting_minutes")
    created_by_user = relationship("User", foreign_keys=[created_by], backref="created_minutes")
    updated_by_user = relationship("User", foreign_keys=[updated_by], backref="updated_minutes")
    attachments = relationship("MinuteAttachment", back_populates="meeting_minute", cascade="all, delete-orphan")
    action_items = relationship("MinuteActionItem", back_populates="meeting_minute", cascade="all, delete-orphan")


class MinuteAttachment(Base):
    """Model for meeting minute attachments (PDFs, images, docs stored in Cloudinary)"""
    __tablename__ = "minute_attachments"

    id = Column(Integer, primary_key=True, index=True)
    meeting_minute_id = Column(Integer, ForeignKey("meeting_minutes.id", ondelete="CASCADE"), nullable=False)
    
    # Cloudinary storage
    cloudinary_public_id = Column(String, nullable=False)  # Cloudinary public ID
    cloudinary_url = Column(String, nullable=False)  # Secure URL from Cloudinary
    resource_type = Column(String, nullable=False)  # image, raw (for PDFs/docs), etc.
    
    # File metadata
    file_name = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # In bytes
    mime_type = Column(String, nullable=False)
    
    # Metadata
    uploaded_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    meeting_minute = relationship("MeetingMinute", back_populates="attachments")
    uploaded_by_user = relationship("User", backref="uploaded_minute_attachments")


class MinuteActionItem(Base):
    """Model for action items derived from meeting minutes"""
    __tablename__ = "minute_action_items"

    id = Column(Integer, primary_key=True, index=True)
    meeting_minute_id = Column(Integer, ForeignKey("meeting_minutes.id", ondelete="CASCADE"), nullable=False)
    
    # Action item details
    description = Column(Text, nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"), nullable=True)  # Optional assignee
    due_date = Column(Date, nullable=True)
    status = Column(String, nullable=False, default="pending")  # pending, in_progress, completed
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    meeting_minute = relationship("MeetingMinute", back_populates="action_items")
    assigned_user = relationship("User", backref="assigned_action_items")
