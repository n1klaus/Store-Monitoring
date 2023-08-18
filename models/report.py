#!/usr/bin/python3

"""Report Class Module"""

from sqlalchemy import Column, Integer, String, ForeignKey, Time, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import enum
from uuid import uuid4
from models.base_class import Base
from core.settings import get_settings

settings = get_settings()

class ReportStatus(enum.Enum):
    """Report status enum"""
    success = "Success"
    fail = "Failed"
    pending = "Pending"
    started = "Started"
    not_started = "Not Started Yet"

class Report(Base):
    """Report Model"""
    __tablename__ = 'reports'

    report_id = Column(UUID(as_uuid=False), primary_key=True, unique=True, default=uuid4)
    name = Column(String)
    reported_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    uptime_last_hour = Column(Time)
    uptime_last_day = Column(Time)
    uptime_last_week = Column(Time)
    downtime_last_hour = Column(Time)
    downtime_last_day = Column(Time)
    downtime_last_week = Column(Time)
    store_id = Column(Integer, ForeignKey("stores.store_id"))
    report_status = Column(Enum(ReportStatus, name='report_status'), nullable=False, default=ReportStatus.not_started)
