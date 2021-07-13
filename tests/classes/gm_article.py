from __future__ import annotations
from jsonclasses import jsonclass, types


def check_owner(article: GMArticle, operator: GMAuthor) -> bool:
    return article.author.id == operator.id


def check_tier(article: GMArticle, operator: GMAuthor) -> bool:
    return operator.paid_user


@jsonclass
class GMAuthor:
    id: str
    name: str
    paid_user: bool
    articles: list[GMArticle] = types.listof('GMArticle').linkedby('author') \
                                     .required


@jsonclass(can_create=[check_owner, check_tier])
class GMArticle:
    name: str
    content: str
    author: GMAuthor
