from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass(validate_all_fields=True)
class UrlAnalysis:
    title: str
    content: str
    cover: str = types.str.url.required
