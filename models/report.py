#!/usr/bin/python3
"""Report Class Module"""
import enum
from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from config import settings
from models.base_class import Base


class ReportStatus(enum.Enum):
    """Report status enum"""

    success = "Success"
    fail = "Failed"
    pending = "Pending"
    started = "Started"
    not_started = "Not Started Yet"


class Report(Base):
    """Report Model"""

    report_id = Column(UUID(as_uuid=False), unique=True)
    name = Column(String)
    reported_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    uptime_last_hour = Column(Time)
    uptime_last_day = Column(Time)
    uptime_last_week = Column(Time)
    downtime_last_hour = Column(Time)
    downtime_last_day = Column(Time)
    downtime_last_week = Column(Time)
    store_id = Column(String, ForeignKey("stores.store_id"))
    report_status = Column(
        Enum(ReportStatus, name="report_status"),
        nullable=False,
        default=ReportStatus.not_started,
    )
