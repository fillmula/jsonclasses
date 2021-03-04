from __future__ import annotations
from jsonclasses import jsonclass


@jsonclass
class SimpleArticle:
    title: str
    content: str
