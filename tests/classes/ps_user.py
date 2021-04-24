from __future__ import annotations
from datetime import datetime
from jsonclasses import jsonclass, types


@jsonclass
class PsUserN:
    username: str
    updated_at: datetime = types.datetime.setonsave(lambda: None).required


@jsonclass
class PsUserV:
    username: str
    updated_at: datetime = types.datetime.setonsave(datetime.now).required


@jsonclass
class PsUserD:
    username: str
    updated_at: int = types.datetime.setonsave(lambda: 2) \
                           .setonsave(lambda x: x * 2)


@jsonclass
class PsUserT:
    username: str
    updated_at: int = types.datetime.setonsave(lambda: 2) \
                           .setonsave(lambda x: x * 2) \
                           .setonsave(lambda x: x + 1)


@jsonclass
class PsUserE:
    username: str
    updated_at: int = types.datetime.setonsave(lambda: 2) \
                           .validate(lambda x: "wrong") \
                           .setonsave(lambda x: x * 2) \
                           .setonsave(lambda x: x + 1)


@jsonclass
class PsUserE2:
    username: str
    updated_at: int = types.datetime.setonsave(lambda: 2) \
                           .setonsave(lambda x: x * 2) \
                           .validate(lambda x: "wrong") \
                           .setonsave(lambda x: x + 1)


@jsonclass
class PsUserE3:
    username: str
    updated_at: int = types.datetime.setonsave(lambda: 2) \
                           .setonsave(lambda x: x * 2) \
                           .setonsave(lambda x: x + 1) \
                           .validate(lambda x: "wrong")


@jsonclass
class PsUserCV:
    username: str
    updated_at: int = types.datetime \
                           .setonsave(lambda: 2).validate(lambda x: None) \
                           .setonsave(lambda x: x * 2).validate(lambda x: None) \
                           .setonsave(lambda x: x + 1).validate(lambda x: None)


@jsonclass
class PsUserL:
    counts: list[int] = types.listof(types.int.setonsave(lambda s: s + 1))


@jsonclass
class PsUserLE:
    counts: list[int] = types.listof(types.int.setonsave(lambda s: None))


@jsonclass
class PsUserDI:
    counts: dict[str, int] = types.dictof(types.int.setonsave(lambda s: s + 1))


@jsonclass
class PsUserDE:
    counts: dict[str, int] = types.dictof(types.int.setonsave(lambda s: None))


@jsonclass
class PsUserS:
    counts: dict[str, int] = types.shape({
        'a': types.int.setonsave(lambda x: x + 1),
        'b': types.int.setonsave(lambda x: x + 1)})


@jsonclass
class PsUserSE:
    counts: dict[str, int] = types.shape({
        'a': types.int.setonsave(lambda x: x + 1),
        'b': types.int.setonsave(lambda x: None).required})
