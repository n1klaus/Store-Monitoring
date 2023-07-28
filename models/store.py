#!/usr/bin/python3

"""Store Class Module"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time, Enum
from sqlalchemy.dialects.postgresql import ARRAY, BOOLEAN
from sqlalchemy.sql import func
import enum
import pytz
from models.base_model import BaseModel
from utils.settings import get_settings

settings = get_settings()

DEFAULT_TZ = str(pytz.timezone(settings.DEFAULT_TZ))

WORKING_DAYS = [False, False, False, False, False, False, False]

class StoreStatus(enum.Enum):
    """Store Status Enum"""
    online = 'Online'
    offline = 'Offline'


class Store(BaseModel):
    """Store Model"""
    __tablename__ = 'stores'

    store_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    last_read_timestamp = Column(DateTime(timezone=True), nullable=False, default=func.now())
    timezone = Column(String, default=DEFAULT_TZ)
    opening_time = Column(Time)
    closing_time = Column(Time)
    working_days_of_week = Column(ARRAY(BOOLEAN), default=WORKING_DAYS)
    last_known_uptime_utc = Column(DateTime(timezone=True))
    last_known_downtime_utc = Column(DateTime(timezone=True))
    store_status = Column(Enum(StoreStatus, name='store_status'), nullable=False, default=StoreStatus.online)
    owner_id = Column(Integer, ForeignKey('owners.owner_id'))


