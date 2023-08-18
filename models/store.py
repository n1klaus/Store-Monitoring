#!/usr/bin/python3

"""Store Class Module"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time, Enum
from sqlalchemy.dialects.postgresql import ARRAY, BOOLEAN
from sqlalchemy.sql import func
from datetime import time
import enum
import pytz
from models.base_class import Base
from core.settings import get_settings
from utils.csv_handler import CSVHandler

settings = get_settings()

DEFAULT_TZ = str(pytz.timezone(settings.DEFAULT_TZ))

WORKING_DAYS = [True, True, True, True, True, True, True]

class StoreStatus(enum.Enum):
    """Store Status Enum"""
    online = 'Online'
    offline = 'Offline'


class Store(Base):
    """Store Model"""
    __tablename__ = 'stores'

    store_id = Column(String, primary_key=True, unique=True)
    timestamp_utc = Column(DateTime(timezone=True), nullable=False, default=func.now())
    timezone = Column(String, default=DEFAULT_TZ)
    opening_time = Column(Time, default=time(0, 0, 0))
    closing_time = Column(Time, default=time(23, 59, 59))
    working_days_of_week = Column(ARRAY(BOOLEAN), default=WORKING_DAYS)
    last_known_uptime_utc = Column(DateTime(timezone=True))
    last_known_downtime_utc = Column(DateTime(timezone=True))
    store_status = Column(Enum(StoreStatus, name='store_status'), nullable=False, default=StoreStatus.online)
    owner_id = Column(Integer, ForeignKey('owners.owner_id'))

    def get_online_stats(self):
        """"""
        return self.store_id, self.last_known_uptime_utc, self.last_known_downtime_utc, self.store_status
