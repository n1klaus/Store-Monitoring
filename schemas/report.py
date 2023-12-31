#!/usr/bin/python3
from datetime import time

from pydantic import BaseModel


class ReportView(BaseModel):
    """Schema for viewing report"""

    store_id: int
    uptime_last_hour: time
    uptime_last_day: time
    uptime_last_week: time
    downtime_last_hour: time
    downtime_last_day: time
    downtime_last_week: time
