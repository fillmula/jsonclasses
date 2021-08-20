"""This module defines JSON Class context objects."""
from __future__ import annotations
from typing import Any, NamedTuple, Union, TYPE_CHECKING
from .types import types
from .mgraph import MGraph
if TYPE_CHECKING:
    from .cdef import Cdef
    from .fdef import Fdef
    from .jobject import JObject


class CtxCfg(NamedTuple):

    all_fields: bool = False
    """On validating, whether validate all fields.
    """

    ignore_writeonly: bool = False
    """On tojson, whether ignore writeonly.
    """

    fill_dest_blanks: bool = False
    """On setting, whether fill default fields with None value.
    """

class Ctx(NamedTuple):
    root: JObject
    owner: JObject
    parent: Union[list, dict, JObject]
    value: Any
    original: Any
    ctxcfg: CtxCfg
    keypatho: list[Union[str, int]]
    keypathr: list[Union[str, int]]
    keypathp: list[Union[str, int]]
    fdef: Fdef
    operator: Any
    mgraph: MGraph = MGraph()
    idchain: list[str] = []

    @property
    def cdefroot(self: Ctx) -> Cdef:
        return self.root.__class__.cdef

    @property
    def cdefowner(self: Ctx) -> Cdef:
        return self.owner.__class__.cdef

    @property
    def iscreate(self: Ctx) -> bool:
        return self.original is None

    @classmethod
    def rootctx(cls: type[Ctx], root: JObject, ctxcfg: CtxCfg,
                value: Any = None) -> Ctx:
        return Ctx(root=root, owner=root, parent=root, value=value or root,
                   original=root, ctxcfg=ctxcfg, keypatho=[], keypathr=[],
                   keypathp=[], fdef=types.objof(root.__class__).fdef,
                   operator=root._operator, mgraph=MGraph(), idchain=[])
