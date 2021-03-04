from __future__ import annotations
from typing import Optional
from datetime import date
from jsonclasses import jsonclass


@jsonclass
class SimpleDeadline:
    ended_at: Optional[date]
    message: Optional[str]
