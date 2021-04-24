from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class EvUser:
    username: str = types.str.required
    password: str = types.str.minlength(8).maxlength(16) \
                         .transform(lambda s: s + '0x0x').required


@jsonclass
class EvUserL:
    passwords: list[str] = types.listof(
        types.str.minlength(2).maxlength(4)
                 .transform(lambda s: s + '0x0x0x0x'))


@jsonclass
class EvUserD:
    passwords: dict[str, str] = types.dictof(
        types.str.minlength(2).maxlength(4)
                 .transform(lambda s: s + '0x0x0x0x'))


@jsonclass
class EvUserS:
    passwords: dict[str, str] = types.shape({
        'a': types.str.minlength(2).maxlength(4)
                      .transform(lambda s: s + '0x0x0x0x'),
        'b': types.str.minlength(2).maxlength(4)
                      .transform(lambda s: s + '0x0x0x0x')})
