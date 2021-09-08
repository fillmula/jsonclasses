from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class ListDict:
    numbers: list[dict[str, int]] = types.nonnull.listof(dict[str, int])
