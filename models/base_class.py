#!/usr/bin/python3
"""Base Class Module"""
import enum
from copy import deepcopy

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import Sequence
from sqlalchemy.orm import as_declarative
from sqlalchemy.orm import declared_attr
from sqlalchemy.sql import func


class SystemStatus(enum.Enum):
    """Base model status enum"""

    active = "Active"
    inactive = "Inactive"


@as_declarative()
class Base:
    """Base Class"""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

    id = Column(Integer, Sequence(name="base_id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    sys_status = Column(
        Enum(SystemStatus, name="sys_status"), default=SystemStatus.active
    )

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the object"""
        my_dict: dict = deepcopy(self.__dict__)
        del my_dict["_sa_instance_state"]
        return my_dict

    def __repr__(self):
        """ "Return the canonical representation of the object"""
        return f"{self.id} {self.to_dict()}"
