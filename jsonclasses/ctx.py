"""This module defines JSON Class context objects."""
from __future__ import annotations
from typing import Any, NamedTuple, Union, Optional, TYPE_CHECKING
from .types import types
from .mgraph import MGraph
if TYPE_CHECKING:
    from .cdef import Cdef
    from .fdef import Fdef
    from .jobject import JObject


class CtxCfg(NamedTuple):

    all_fields: Optional[bool] = None
    """On validating, whether validate all fields.
    """

    ignore_writeonly: Optional[bool] = False
    """On tojson, whether ignore writeonly.
    """

    fill_dest_blanks: Optional[bool] = False
    """On setting, whether fill default fields with None value.
    """

class Ctx(NamedTuple):
    root: JObject
    owner: JObject
    parent: Union[list, dict, JObject]
    value: Any
    original: Any
    ctxcfg: CtxCfg
    keypathr: list[Union[str, int]]
    keypatho: list[Union[str, int]]
    keypathp: list[Union[str, int]]
    fdef: Fdef
    operator: Any
    mgraph: MGraph = MGraph()
    idchain: list[str] = []

    @property
    def val(self: Ctx) -> Any:
        return self.value

    @property
    def cdefroot(self: Ctx) -> Cdef:
        return self.root.__class__.cdef

    @property
    def cdefowner(self: Ctx) -> Cdef:
        return self.owner.__class__.cdef

    @property
    def iscreate(self: Ctx) -> bool:
        return self.original is None

    @property
    def skeypathr(self: Ctx) -> str:
        return '.'.join([str(k) for k in self.keypathr])

    @property
    def skeypatho(self: Ctx) -> str:
        return '.'.join([str(k) for k in self.keypatho])

    @property
    def skeypathp(self: Ctx) -> str:
        return '.'.join([str(k) for k in self.keypathp])

    @classmethod
    def rootctx(cls: type[Ctx], root: JObject, ctxcfg: CtxCfg,
                value: Any = None) -> Ctx:
        fdef = types.objof(root.__class__).fdef
        fdef._cdef = root.__class__.cdef
        return Ctx(root=root, owner=root, parent=root, value=value or root,
                   original=root, ctxcfg=ctxcfg, keypatho=[], keypathr=[],
                   keypathp=[], fdef=fdef,
                   operator=root._operator, mgraph=MGraph(), idchain=[])

    def nval(self: Ctx, newval: Any) -> Ctx:
        return Ctx(root=self.root, owner=self.owner, parent=self.parent,
                   value=newval, original=self.original, ctxcfg=self.ctxcfg,
                   keypatho=self.keypatho, keypathr=self.keypathr,
                   keypathp=self.keypathp, fdef=self.fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain)

    def nextv(self: Ctx, val: Any, key: str | int, fdef: Fdef) -> Ctx:
        return Ctx(root=self.root, owner=self.owner, parent=self.parent,
                   value=val, original=None, ctxcfg=self.ctxcfg,
                   keypatho=[*self.keypatho, key],
                   keypathr=[*self.keypathr, key],
                   keypathp=[*self.keypathp, key], fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain)

    def nexto(self: Ctx, val: Any, key: str | int, fdef: Fdef) -> Ctx:
        return Ctx(root=self.root, owner=val, parent=val, value=val,
                   original=None, ctxcfg=self.ctxcfg, keypatho=[],
                   keypathr=[*self.keypathr, key], keypathp=[], fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain)

    def nextvc(self: Ctx, val: Any, key: str | int, fdef: Fdef, c: str) -> Ctx:
        return Ctx(root=self.root, owner=self.owner, parent=self.parent,
                   value=val, original=None, ctxcfg=self.ctxcfg,
                   keypatho=[*self.keypatho, key],
                   keypathr=[*self.keypathr, key],
                   keypathp=[*self.keypathp, key], fdef=fdef, operator=self.operator,
                   mgraph=self.mgraph, idchain=[*self.idchain, c])

    def nextoc(self: Ctx, val: Any, key: str | int, fdef: Fdef, c: str) -> Ctx:
        return Ctx(root=self.root, owner=val, parent=val,
                   value=val, original=None, ctxcfg=self.ctxcfg,
                   keypatho=[], keypathr=[*self.keypathr, key],
                   keypathp=[], fdef=fdef, operator=self.operator,
                   mgraph=self.mgraph, idchain=[*self.idchain, c])

    def colval(self: Ctx, val: Any, key: str | int, fdef: Fdef, p: Any) -> Ctx:
        return Ctx(root=self.root, owner=self.owner, parent=p,
                   value=val, original=None, ctxcfg=self.ctxcfg,
                   keypatho=[*self.keypatho, key],
                   keypathr=[*self.keypathr, key],
                   keypathp=[key], fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain)

    def default(self: Ctx, owner: JObject, key: str | int, fdef: Fdef) -> Ctx:
        return Ctx(root=self.root, owner=owner, parent=owner, value=None,
                   original=None, ctxcfg=self.ctxcfg,
                   keypatho=[*self.keypatho, key],
                   keypathr=[*self.keypathr, key],
                   keypathp=[*self.keypathp, key], fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain)
