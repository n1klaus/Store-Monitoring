#!/usr/bin/python3
from datetime import datetime
from datetime import time
from datetime import timezone
from enum import Enum
from typing import List

from pydantic import BaseModel
from sqlalchemy.dialects.postgresql import TIMESTAMP


class StoreView(BaseModel):
    """Schema for viewing store"""

    store_id: int
    timestamp_utc: TIMESTAMP
    timezone: timezone
    opening_time_utc: time
    closing_time_utc: time
    opening_time_local: time
    closing_time_local: time
    working_days_of_week: List[bool]
    last_known_uptime_utc: datetime
    last_known_downtime_utc: datetime
    status: Enum
