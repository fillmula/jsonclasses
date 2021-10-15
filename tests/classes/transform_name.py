from __future__ import annotations
from typing import Optional
from jsonclasses import jsonclass, types


@jsonclass
class TransformName:
    name: Optional[str] = types.str.transform(lambda s: s + 'q')


@jsonclass
class CTransformName:
    name: Optional[str] = types.str.transform(lambda s, c: s + c.val)


@jsonclass
class TTransformName:
    age: Optional[int] = types.int.transform(types.add(5).mul(5))
