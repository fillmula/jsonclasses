from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class OpUser:
    name: str = types.str.required
    owned_teams: list[OpTeam] = types.nonnull.listof('OpTeam') \
                                     .linkedby('owner')


@jsonclass
class OpTeam:
    name: str = types.str.op(lambda o, t: o == t.owner).required
    owner: OpUser = types.instanceof('OpUser').linkto.required


@jsonclass
class AsopUser:
    name: str = types.str.required
    owned_teams: list[AsopTeam] = types.nonnull.listof('AsopTeam') \
                                       .linkedby('owner')


@jsonclass
class AsopTeam:
    name: str = types.str.required
    owner: AsopUser = types.instanceof('AsopUser').linkto.asop(lambda o: o)


@jsonclass
class AsopdUser:
    name: str = types.str.required
    owned_teams: list[AsopdTeam] = types.nonnull.listof('AsopdTeam') \
                                        .linkedby('owner')


@jsonclass
class AsopdTeam:
    name: str = types.str.required
    owner: AsopdUser = types.instanceof('AsopdUser').linkto.asopd
