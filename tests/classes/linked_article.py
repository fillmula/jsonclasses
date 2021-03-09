from __future__ import annotations
from typing import TYPE_CHECKING
from jsonclasses import jsonclass, Link, linkto
if TYPE_CHECKING:
    from tests.classes.linked_author import LinkedAuthor


@jsonclass
class LinkedArticle:
    name: str
    author: Link[LinkedAuthor, linkto]
