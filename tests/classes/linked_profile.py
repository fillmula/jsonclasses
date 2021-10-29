from __future__ import annotations
from typing import Annotated, TYPE_CHECKING
from jsonclasses import jsonclass, linkto
if TYPE_CHECKING:
    from tests.classes.linked_user import LinkedUser, LinkedUserN


@jsonclass
class LinkedProfile:
    name: str
    user: Annotated[LinkedUser, linkto]


@jsonclass(output_null=True)
class LinkedProfileN:
    name: str
    user: Annotated[LinkedUserN, linkto]
