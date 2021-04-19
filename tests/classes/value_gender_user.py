from __future__ import annotations
from enum import Enum
from jsonclasses import jsonclass, jsonenum, types


@jsonenum
class ValueGender(Enum):
    MALE = 1
    FEMALE = 2


@jsonclass
class ValueGenderUser:
    name: str = types.str.required
    gender: ValueGender = types.enum(ValueGender).inputvalue.outputvalue \
                               .required
