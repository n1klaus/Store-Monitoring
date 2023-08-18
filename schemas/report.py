#!/usr/bin/python3

from pydantic import BaseModel
from typing import Optional

class ReportView(BaseModel):
    """Schema for viewing report"""
    store_id: int
    uptime_last_hour: int
    uptime_last_day: int
    uptime_last_week: int
    downtime_last_hour: int
    downtime_last_day: int
    downtime_last_week: int
