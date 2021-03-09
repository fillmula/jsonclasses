from __future__ import annotations
from typing import TYPE_CHECKING
from jsonclasses import jsonclass, Link, linkedby
if TYPE_CHECKING:
    from tests.classes.linked_article import LinkedArticle


@jsonclass
class LinkedAuthor:
    name: str
    articles: Link[list[LinkedArticle], linkedby('author')]
