#!/usr/bin/python3
from datetime import datetime
from typing import List

from pydantic import BaseModel


class OwnerView(BaseModel):
    """Schema for viewing an owner"""

    name: str
    email: str
    phone: str


class OwnerCreate(OwnerView):
    """Schema for creating an owner"""

    owner_id: int
    last_login_utc: datetime
    owned_stores: List[int]
