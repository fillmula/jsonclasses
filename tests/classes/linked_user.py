from __future__ import annotations
from typing import TYPE_CHECKING
from jsonclasses import jsonclass, Link, linkedby
if TYPE_CHECKING:
    from tests.classes.linked_profile import LinkedProfile


@jsonclass
class LinkedUser:
    name: str
    profile: Link[LinkedProfile, linkedby('user')]
