from __future__ import annotations
from jsonclasses import jsonclass, types


def create_first_revision(article: CBArticle) -> None:
    CBRevision(name='First').article = article


@jsonclass
class CBRevision:
    name: str
    article: CBArticle = types.instanceof('CBArticle').linkto.required


@jsonclass(on_create=create_first_revision)
class CBArticle:
    name: str
    content: str
    revisions: list[CBRevision] = types.nonnull.listof('CBRevision') \
                                       .linkedby('article')
