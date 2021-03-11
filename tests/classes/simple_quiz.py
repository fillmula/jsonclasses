from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class SimpleQuiz:
    numbers: dict[str, int] = types.dictof(types.int.min(100))
