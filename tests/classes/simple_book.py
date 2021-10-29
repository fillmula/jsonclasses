from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class SimpleBook:
    name: Optional[str]
    published: bool = types.bool.default(False)


@jsonclass(output_null=True)
class SimpleBookN:
    name: Optional[str]
    published: bool = types.bool.default(False)
