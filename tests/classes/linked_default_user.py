from __future__ import annotations
from typing import TYPE_CHECKING
from jsonclasses import jsonclass, Link, linkedthru, types
if TYPE_CHECKING:
    from tests.classes.linked_default_post import LinkedDefaultPost


@jsonclass
class LinkedDefaultUser:
    name: str = types.str.default('Default User')
    posts: Link[list[LinkedDefaultPost], linkedthru('users')]
