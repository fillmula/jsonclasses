from __future__ import annotations
from typing import Optional
from datetime import datetime
from jsonclasses import jsonclass


@jsonclass
class SimpleBalance:
    date: Optional[datetime]
    balance: Optional[float]
