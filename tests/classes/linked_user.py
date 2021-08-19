from __future__ import annotations
from typing import Annotated, TYPE_CHECKING
from jsonclasses import jsonclass, linkedby
if TYPE_CHECKING:
    from tests.classes.linked_profile import LinkedProfile


@jsonclass
class LinkedUser:
    name: str
    profile: Annotated[LinkedProfile, linkedby('user')]
