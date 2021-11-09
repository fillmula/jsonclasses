from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class LinkedOwner:
    id: str = types.str.primary.required
    permissions: list[LinkedPermission] = types.listof('LinkedPermission').linkedby('owner')


@jsonclass(
    can_read=types.getop.isobj(types.this.fval('owner'))
)
class LinkedPermission:
    id: str = types.str.primary.required
    owner: LinkedOwner = types.objof('LinkedOwner').linkto.required
