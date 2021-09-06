from __future__ import annotations
from typing import Any
from jsonclasses import jsonclass, types


@jsonclass
class AnyArticle:
    title: Any
    content: Any = types.any.required
