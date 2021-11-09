from typing import NamedTuple


class ObjRef(NamedTuple):
    cls: str
    id: str | int
