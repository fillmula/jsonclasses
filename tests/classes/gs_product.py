from __future__ import annotations
from jsonclasses import jsonclass, types


def check_user(product: GSProduct, operator: GSProductUser) -> bool:
    return product.user.id == operator.id and operator.paid_user


@jsonclass
class GSProductUser:
    id: str
    name: str
    paid_user: bool
    books: list[GSProduct] = types.nonnull.listof('GSProduct').linkedby('user')


@jsonclass(can_delete=check_user, can_read=check_user)
class GSProduct:
    name: str
    user: GSProductUser = types.instanceof('GSProductUser').linkto.required
