#!/usr/bin/python3
"""Owner Class Module"""
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from models.base_class import Base


class Owner(Base):
    """Owner Model"""

    owner_id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    last_login_time = Column(DateTime(timezone=True))
    stores = relationship("Store", backref="owner")
