from __future__ import annotations
from typing import TYPE_CHECKING
from jsonclasses import jsonclass, Link, linkto
if TYPE_CHECKING:
    from tests.classes.linked_user import LinkedUser


@jsonclass
class LinkedProfile:
    name: str
    user: Link[LinkedUser, linkto]
