from __future__ import annotations
from jsonclasses import jsonclass, types


def check_author(article: GSArticle, operator: GSAuthor) -> bool:
    return article.author.id == operator.id and operator.paid_user


@jsonclass
class GSAuthor:
    id: str
    name: str
    paid_user: bool
    articles: list[GSArticle] = types.listof('GSArticle').linkedby('author') \
                                     .required


@jsonclass(can_create=check_author)
class GSArticle:
    name: str
    content: str
    author: GSAuthor
