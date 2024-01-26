#!/usr/bin/python3
"""Store Class Module"""
import enum
from datetime import time

import pytz
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import BOOLEAN
from sqlalchemy.sql import func

from config import settings
from models.base_class import Base

DEFAULT_TZ = str(pytz.timezone(settings.DEFAULT_TZ))

WORKING_DAYS = [True, True, True, True, True, True, True]


class StoreStatus(enum.Enum):
    """Store Status Enum"""

    online = "Online"
    offline = "Offline"


class Store(Base):
    """Store Model"""

    store_id = Column(String, primary_key=True, unique=True)
    timestamp_utc = Column(DateTime(timezone=True), nullable=False, default=func.now())
    timezone = Column(String, default=DEFAULT_TZ)
    opening_time = Column(Time, default=time(0, 0, 0))
    closing_time = Column(Time, default=time(23, 59, 59))
    working_days_of_week = Column(ARRAY(BOOLEAN), default=WORKING_DAYS)
    last_known_uptime_utc = Column(DateTime(timezone=True))
    last_known_downtime_utc = Column(DateTime(timezone=True))
    store_status = Column(
        Enum(StoreStatus, name="store_status"),
        nullable=False,
        default=StoreStatus.online,
    )
    owner_id = Column(Integer, ForeignKey("owners.owner_id"))

    def get_online_stats(self):
        """"""
        return (
            self.store_id,
            self.last_known_uptime_utc,
            self.last_known_downtime_utc,
            self.store_status,
        )
