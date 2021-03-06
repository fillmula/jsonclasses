from __future__ import annotations
from jsonclasses import jsonclass, types
from tests.classes.article import Article


@jsonclass
class Author:
    name: str
    articles: list[Article] = types.listof('Article').linkedby('author') \
                                   .required
