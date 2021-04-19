from __future__ import annotations
from enum import Enum
from jsonclasses import jsonclass, jsonenum, types


@jsonenum
class Gender(Enum):
    MALE = 1
    FEMALE = 2


@jsonclass
class EnumUser:
    name: str = types.str.required
    gender: Gender = types.enum(Gender).required
