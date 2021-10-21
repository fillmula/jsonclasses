from __future__ import annotations
from jsonclasses import jsonclass, types


@jsonclass
class LinkedSong:
    id: int = types.int.primary.required
    name: str
    singers: list[LinkedSinger] = types.nonnull.listof('LinkedSinger').linkto


@jsonclass
class LinkedSinger:
    id: int = types.int.primary.required
    name: str
    songs: list[LinkedSong] = types.nonnull.listof('LinkedSong').linkedby('singers')
