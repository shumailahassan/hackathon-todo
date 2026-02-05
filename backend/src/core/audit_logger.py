import logging
from enum import Enum
from datetime import datetime
from typing import Optional, Dict, Any
import json
import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, String, DateTime, Text, Integer
from sqlmodel import SQLModel, Field

# Configure audit logger
audit_logger = logging.getLogger("audit")
audit_logger.setLevel(logging.INFO)

# Create audit handler if it doesn't exist
if not audit_logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - AUDIT - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    audit_logger.addHandler(handler)
    audit_logger.propagate = False  # Prevent propagation to root logger


class AuditAction(str, Enum):
    """Enumeration of possible audit actions"""
    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"


class AuditLog(SQLModel, table=True):
    """Audit log model for tracking user actions"""
    __tablename__ = "audit_log"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(index=True)
    action: str = Field(sa_column=Column(String(20)))  # Using AuditAction values
    resource_type: str = Field(sa_column=Column(String(50)))
    resource_id: Optional[str] = Field(default=None)
    ip_address: Optional[str] = Field(default=None)
    user_agent: Optional[str] = Field(default=None)
    details: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(Text))
    timestamp: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True), index=True))


async def log_audit_event(
    db: AsyncSession,
    user_id: uuid.UUID,
    action: AuditAction,
    resource_type: str,
    resource_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
):
    """
    Log an audit event to the database and file system

    Args:
        db: Database session
        user_id: ID of the user performing the action
        action: Type of action being performed
        resource_type: Type of resource being acted upon
        resource_id: ID of the specific resource (optional)
        ip_address: Client IP address (optional)
        user_agent: Client user agent string (optional)
        details: Additional details about the action (optional)
    """
    try:
        # Log to file
        log_details = {
            "user_id": str(user_id),
            "action": action.value,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "details": details
        }
        audit_logger.info(json.dumps(log_details))

        # Optionally save to database as well
        audit_record = AuditLog(
            user_id=user_id,
            action=action.value,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip_address,
            user_agent=user_agent,
            details=details
        )

        db.add(audit_record)
        # Note: We don't commit here as this is meant to be part of the parent transaction
        # or it should be committed separately in a non-blocking way

    except Exception as e:
        # Never let audit logging break the main operation
        audit_logger.error(f"Failed to log audit event: {str(e)}")


# Convenience functions for common audit actions
async def log_data_create(
    db: AsyncSession,
    user_id: uuid.UUID,
    data_id: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
):
    """Log a data creation event"""
    await log_audit_event(
        db, user_id, AuditAction.CREATE, "UserData", data_id, ip_address, user_agent, details
    )


async def log_data_read(
    db: AsyncSession,
    user_id: uuid.UUID,
    data_id: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
):
    """Log a data read event"""
    await log_audit_event(
        db, user_id, AuditAction.READ, "UserData", data_id, ip_address, user_agent, details
    )


async def log_data_update(
    db: AsyncSession,
    user_id: uuid.UUID,
    data_id: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
):
    """Log a data update event"""
    await log_audit_event(
        db, user_id, AuditAction.UPDATE, "UserData", data_id, ip_address, user_agent, details
    )


async def log_data_delete(
    db: AsyncSession,
    user_id: uuid.UUID,
    data_id: str,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None
):
    """Log a data deletion event"""
    await log_audit_event(
        db, user_id, AuditAction.DELETE, "UserData", data_id, ip_address, user_agent, details
    )


async def log_user_login(
    db: AsyncSession,
    user_id: uuid.UUID,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
):
    """Log a user login event"""
    await log_audit_event(
        db, user_id, AuditAction.LOGIN, "User", str(user_id), ip_address, user_agent
    )


async def log_user_logout(
    db: AsyncSession,
    user_id: uuid.UUID,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None
):
    """Log a user logout event"""
    await log_audit_event(
        db, user_id, AuditAction.LOGOUT, "User", str(user_id), ip_address, user_agent
    )