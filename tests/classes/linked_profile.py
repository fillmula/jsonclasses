from __future__ import annotations
from typing import Annotated, TYPE_CHECKING
from jsonclasses import jsonclass, linkto
if TYPE_CHECKING:
    from tests.classes.linked_user import LinkedUser


@jsonclass
class LinkedProfile:
    name: str
    user: Annotated[LinkedUser, linkto]
