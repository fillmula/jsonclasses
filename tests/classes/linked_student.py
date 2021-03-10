from __future__ import annotations
from typing import TYPE_CHECKING
from jsonclasses import jsonclass, types
if TYPE_CHECKING:
    from tests.classes.linked_school import LinkedSchool


@jsonclass
class LinkedStudent:
    name: str
    school: LinkedSchool = types.linkto.instanceof('LinkedSchool').present
