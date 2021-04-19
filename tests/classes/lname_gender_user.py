from __future__ import annotations
from enum import Enum
from jsonclasses import jsonclass, jsonenum, types


@jsonenum
class LnameGender(Enum):
    MALE = 1
    FEMALE = 2


@jsonclass
class LnameGenderUser:
    name: str = types.str.required
    gender: LnameGender = types.enum(LnameGender).inputlname.outputlname \
                               .required
