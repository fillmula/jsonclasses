from __future__ import annotations
from typing import Annotated, TYPE_CHECKING
from jsonclasses import jsonclass, linkedby
if TYPE_CHECKING:
    from tests.classes.linked_article import LinkedArticle


@jsonclass
class LinkedAuthor:
    name: str
    articles: Annotated[list[LinkedArticle], linkedby('author')]
