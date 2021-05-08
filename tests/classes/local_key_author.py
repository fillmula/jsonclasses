from __future__ import annotations
from jsonclasses import jsonclass, types


__id = 0


def nextid():
    global __id
    __id = __id + 1
    return __id


@jsonclass
class LKAuthor:
    id: int = types.int.readonly.primary.default(nextid).required
    name: str
    articles: list[LKArticle] = types.listof('LKArticle').linkedby('author')


@jsonclass
class LKArticle:
    id: int = types.int.readonly.primary.default(nextid).required
    name: str
    author: LKAuthor = types.instanceof(LKAuthor).linkto
