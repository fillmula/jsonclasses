from __future__ import annotations
from typing import TYPE_CHECKING
from jsonclasses import jsonclass, types
if TYPE_CHECKING:
    from tests.classes.article import Article


@jsonclass
class Author:
    name: str
    articles: list[Article] = types.listof('Article').linkedby('author') \
                                   .required
