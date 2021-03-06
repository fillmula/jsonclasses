from __future__ import annotations
from jsonclasses import jsonclass
from tests.funcs.yet_another_key_transformer import yet_another_key_transformer


@jsonclass(strict_input=False)
class SimpleTenant:
    name: str
    age: int
