from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class ListQuiz:
    numbers: list[int] = types.listof(types.int.min(100))
