from __future__ import annotations
from typing import TYPE_CHECKING
from jsonclasses import jsonclass, types
if TYPE_CHECKING:
    from tests.classes.author import Author


@jsonclass(strict_input=False, validate_all_fields=True)
class Article:
    title: str
    content: str
    author: Author = types.instanceof('Author').linkto.required
