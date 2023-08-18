#!/usr/bin/python3

from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import TIMESTAMP, TIME, ENUM, INTEGER, BOOLEAN
from sqlalchemy import DateTime
from time import time
from datetime import datetime, timezone
from typing import List


class StoreView(BaseModel):
    """Schema for viewing store"""
    store_id: INTEGER
    timestamp_utc: TIMESTAMP
    timezone: timezone
    opening_time_utc: TIME
    closing_time_utc: TIME
    opening_time_local: TIME
    closing_time_local: TIME
    working_days_of_week: List[BOOLEAN]
    last_known_uptime_utc: DateTime
    last_known_downtime_utc: DateTime
    status: ENUM
