from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class LinkedUserSOS:
    id: int = types.int.primary.required
    name: str = types.str.required
    value: int = types.int.setonsave(lambda x: x + 1).required
    books: list[LinkedBookSOS] = types.nonnull.listof('LinkedBookSOS') \
                                      .linkedby('user').required


@jsonclass
class LinkedBookSOS:
    id: int = types.int.primary.required
    name: str = types.str.required
    value: int = types.int.setonsave(lambda x: x + 1).required
    user: LinkedUserSOS = types.linkto.instanceof(LinkedUserSOS).required


@jsonclass
class LinkedUserSOSE:
    id: int = types.int.primary.required
    name: str = types.str.required
    value: int = types.int.setonsave(lambda x: x + 1).required
    books: list[LinkedBookSOSE] = types.nonnull.listof('LinkedBookSOSE') \
                                       .embedded.required


@jsonclass
class LinkedBookSOSE:
    id: int = types.int.primary.required
    name: str = types.str.required
    value: int = types.int.setonsave(lambda x: x + 1).required
