from __future__ import annotations
from jsonclasses import jsonclass, types


def check_owner(product: GMProduct, operator: GMProductUser) -> bool:
    return product.user.id == operator.id


def check_tier(product: GMProduct, operator: GMProductUser) -> bool:
    return operator.paid_user


@jsonclass
class GMProductUser:
    id: str
    name: str
    paid_user: bool
    books: list[GMProduct] = types.nonnull.listof('GMProduct').linkedby('user')


@jsonclass(can_delete=[check_owner, check_tier], can_read=[check_owner, check_tier])
class GMProduct:
    name: str
    user: GMProductUser = types.instanceof('GMProductUser').linkto.required
