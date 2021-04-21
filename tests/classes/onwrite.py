from __future__ import annotations
from typing import Any
from jsonclasses import jsonclass, types

val = 0


def check_value() -> int:
    return val


def callback() -> None:
    global val
    val = val + 1


def callbackd(value: int) -> None:
    global val
    val = val + value


def callbackt(value: int, context: Any) -> None:
    global val
    val = val + value + context.value


@jsonclass
class OnwriteSingle:
    a: str = types.str.required
    b: int = types.int.onwrite(callback).required


@jsonclass
class OnwriteDouble:
    a: str = types.str.required
    b: int = types.int.onwrite(callbackd).required


@jsonclass
class OnwriteTriple:
    a: str = types.str.required
    b: int = types.int.onwrite(callbackt).required
