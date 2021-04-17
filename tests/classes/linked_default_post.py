from __future__ import annotations
from typing import TYPE_CHECKING
from jsonclasses import jsonclass, Link, linkedthru, types
if TYPE_CHECKING:
    from tests.classes.linked_default_user import LinkedDefaultUser


@jsonclass
class LinkedDefaultPost:
    name: str = types.str.default('Untitled')
    users: Link[list[LinkedDefaultUser], linkedthru('posts')]
