from __future__ import annotations
from jsonclasses import jsonclass, types


def create_first_revision(article: CBMArticle) -> None:
    CBMRevision(name='First').article = article


def force_content(article: CBMArticle) -> None:
    article.content = 'UPDATED'


@jsonclass
class CBMRevision:
    name: str
    article: CBMArticle = types.instanceof('CBMArticle').linkto.required


@jsonclass(on_create=[create_first_revision, force_content])
class CBMArticle:
    name: str
    content: str
    revisions: list[CBMRevision] = types.nonnull.listof('CBMRevision') \
                                        .linkedby('article')
