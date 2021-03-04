from __future__ import annotations
from typing import Optional
from datetime import datetime
from jsonclasses import jsonclass


@jsonclass(abstract=True)
class AbstractObject:
    id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


@jsonclass
class MyObject(AbstractObject):
    name: Optional[str]
    age: Optional[int]


@jsonclass(abstract=False)
class NonAbstractObject:
    id: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]


@jsonclass
class DefaultNonAbstractObject:
    id: Optional[str]
    created_at: Optional[datetime]
