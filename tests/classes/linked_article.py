from __future__ import annotations
from typing import Annotated, TYPE_CHECKING
from jsonclasses import jsonclass, linkto
if TYPE_CHECKING:
    from tests.classes.linked_author import LinkedAuthor


@jsonclass
class LinkedArticle:
    name: str
    author: Annotated[LinkedAuthor, linkto]
