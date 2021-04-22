from __future__ import annotations
from typing import Optional, Tuple
from jsonclasses import jsonclass, types
from jsonclasses.contexts import ValidatingContext

val = 0
oldval = 0
newval = 0


def check_value() -> int:
    return val


def check_args() -> Tuple[int, int]:
    return (oldval, newval)


def callback(old: int, new: int) -> None:
    global val, oldval, newval
    val = val + 1
    oldval = old
    newval = new


def callbackb(old: int, new: int) -> None:
    global val, oldval, newval
    val = val + 1
    oldval = old
    newval = new
    return new == old + 1


def callbacks(old: int, new: int, context: ValidatingContext) -> None:
    global val, oldval, newval
    val = val + 1
    oldval = old
    newval = new
    if context.value == new + old:
        return None
    else:
        return 'invalid'


@jsonclass
class CompareUser:
    age: int = types.int.compare(callback).required
    name: Optional[str]


@jsonclass
class CompareUserB:
    age: int = types.int.compare(callbackb).required
    name: Optional[str]


@jsonclass
class CompareUserS:
    age: int = types.int.compare(callbacks).required
    name: Optional[str]
