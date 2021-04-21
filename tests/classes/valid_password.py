from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class ValidPassword:
    name: Optional[str]
    password: str = types.str.validate(lambda p: len(p) % 2 == 0).required


@jsonclass
class ValidPasswordMessage:
    name: Optional[str]
    password: str = types.str.validate(lambda p: None if len(p) % 2 == 0
                                       else 'wrong').required


@jsonclass
class CValidPassword:
    name: Optional[str]
    password: str = types.str.validate(lambda p, c: c.value == p).required


@jsonclass
class OptionalPassword:
    name: Optional[str]
    password: Optional[str] = types.str.validate(lambda p: len(p) % 2 == 0)
