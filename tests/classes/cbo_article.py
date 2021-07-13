from __future__ import annotations
from jsonclasses import jsonclass, types


def create_first_revision(article: CBOArticle, operator: str) -> None:
    CBORevision(name=operator).article = article


def force_content(article: CBOArticle, operator: str) -> None:
    article.content = operator


@jsonclass
class CBORevision:
    name: str
    article: CBOArticle = types.instanceof('CBOArticle').linkto.required


@jsonclass(on_create=[create_first_revision, force_content])
class CBOArticle:
    name: str
    content: str
    revisions: list[CBORevision] = types.nonnull.listof('CBORevision') \
                                        .linkedby('article')
