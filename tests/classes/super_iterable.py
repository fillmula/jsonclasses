from __future__ import annotations
from typing import Optional, Any
from jsonclasses import jsonclass, types


@jsonclass
class SuperIterable:
    itsrp: Optional[str] = types.str.replace("abc", "ABC")
    itsr: Optional[str] = types.str.reverse()
    itl: Optional[list[Any]] = types.listof(types.any).reverse()
    itssub: Optional[str] = types.str.replacer("[0-9]", "ABC")
    itssp: Optional[list[str]] = types.split(".").listof(types.str)
    itsj: Optional[str] = types.join('-').str

    itsrpc: Optional[str] = types.str.replace(lambda: "abc", lambda: "ABC")
    itsrpt: Optional[str] = types.str.replace(types.default("abc"), types.default("ABC"))
