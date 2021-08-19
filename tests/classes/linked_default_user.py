from __future__ import annotations
from typing import Annotated, TYPE_CHECKING
from jsonclasses import jsonclass, linkedthru, types
if TYPE_CHECKING:
    from tests.classes.linked_default_post import LinkedDefaultPost


@jsonclass
class LinkedDefaultUser:
    name: str = types.str.default('Default User')
    posts: Annotated[list[LinkedDefaultPost], linkedthru('users')]
