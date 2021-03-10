from __future__ import annotations
from typing import TYPE_CHECKING
from jsonclasses import jsonclass, types
if TYPE_CHECKING:
    from tests.classes.linked_student import LinkedStudent


@jsonclass
class LinkedSchool:
    name: str
    students: list[LinkedStudent] = types.nonnull.listof('LinkedStudent')
