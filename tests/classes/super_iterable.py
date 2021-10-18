from __future__ import annotations
from typing import Optional, Any
from jsonclasses import jsonclass, types


@jsonclass
class SuperIterable:
    itsrp: Optional[str] = types.str.replace("abc", "ABC")
    itsr: Optional[str] = types.str.reverse()
    itl: Optional[list[Any]] = types.listof(types.any).reverse()
    itssub: Optional[str] = types.str.replacer("[0-9]", "ABC")
    c_itssub: Optional[str] = types.str.replacer(lambda: "[0-9]", lambda: "ABC")
    t_itssub: Optional[str] = types.str.replacer(types.default("[0-9]"), types.default("ABC"))

    itssp: Optional[list[str]] = types.split(".").listof(types.str)
    c_itssp: Optional[list[str]] = types.split(lambda: '.').listof(types.str)
    t_itssp: Optional[list[str]] = types.split(types.default('.')).listof(types.str)

    itsj: Optional[str] = types.join('-').str

    itsrpc: Optional[str] = types.str.replace(lambda: "abc", lambda: "ABC")
    itsrpt: Optional[str] = types.str.replace(types.default("abc"), types.default("ABC"))

    c_itsj: Optional[str] = types.join(lambda: '-')
    t_itsj: Optional[str] = types.join(types.default('-'))
