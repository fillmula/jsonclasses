from jsonclasses import jsonclass, types

val = 0
intval = 0


def check_value() -> int:
    return val


def check_args() -> int:
    return intval


def callback(new_value: int) -> None:
    global val, intval
    val = val + 1
    intval = new_value


def callbackz() -> None:
    global val
    val = val + 10


@jsonclass
class UserOnsave:
    name: str = types.str.required
    age: int = types.int.onsave(callback).required


@jsonclass
class UserOnsaveZ:
    name: str = types.str.required
    age: int = types.int.onsave(callbackz).required
