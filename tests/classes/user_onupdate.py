from typing import Tuple
from jsonclasses import jsonclass, types
from jsonclasses.contexts import TransformingContext

val = 0
oldval = -1
newval = -1


def check_value() -> int:
    return val


def check_args() -> Tuple[int, int]:
    return (oldval, newval)


def callback(new_value: int) -> None:
    global val, newval, oldval
    val = val + 1
    newval = new_value
    oldval = -1


def callbackd(old_value: int, new_value: int) -> None:
    global val, newval, oldval
    val = val + 1
    newval = new_value
    oldval = old_value


def callbackt(old_value: int,
              new_value: int,
              context: TransformingContext) -> None:
    global val, newval, oldval
    val = val + 1
    newval = new_value + context.value
    oldval = old_value + context.value


def callbackz() -> None:
    global val, newval, oldval
    val = val + 1
    newval = -50
    oldval = -50


@jsonclass
class UserOnupdate:
    name: str = types.str.required
    age: int = types.int.onupdate(callback).required


@jsonclass
class UserOnupdateD:
    name: str = types.str.required
    age: int = types.int.onupdate(callbackd).required


@jsonclass
class UserOnupdateT:
    name: str = types.str.required
    age: int = types.int.onupdate(callbackt).required


@jsonclass
class UserOnupdateZ:
    name: str = types.str.required
    age: int = types.int.onupdate(callbackz).required
