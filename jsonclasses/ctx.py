"""This module defines JSON Class context objects."""
from __future__ import annotations
from typing import Any, NamedTuple, Union, Optional, TYPE_CHECKING
from .jconf import JConf
from .types import types
from .mgraph import MGraph
from .vmsgcollector import VMsgCollector
from .excs import ValidationException
if TYPE_CHECKING:
    from .cdef import Cdef
    from .fdef import Fdef
    from .jobject import JObject


class CtxCfg(NamedTuple):

    all_fields: Optional[bool] = None
    """On validating, whether validate all fields.
    """

    ignore_writeonly: Optional[bool] = None
    """On tojson, whether ignore writeonly.
    """

    fill_dest_blanks: Optional[bool] = None
    """On setting, whether fill default fields with None value.
    """

class Ctx(NamedTuple):
    root: JObject
    owner: JObject
    parent: Union[list, dict, JObject]
    holder: Optional[JObject]
    val: Any
    original: Any
    ctxcfg: CtxCfg
    keypathr: list[Union[str, int]]
    keypatho: list[Union[str, int]]
    keypathp: list[Union[str, int]]
    keypathh: list[Union[str, int]]
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
    def cdefholder(self: Ctx) -> Cdef:
        return self.holder.__class__.cdef

    @property
    def jconfroot(self: Ctx) -> JConf:
        return self.cdefroot.jconf

    @property
    def jconfowner(self: Ctx) -> JConf:
        return self.cdefowner.jconf

    @property
    def jconfholder(self: Ctx) -> JConf:
        return self.cdefholder.jconf

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

    @property
    def skeypathh(self: Ctx) -> str:
        return '.'.join([str(k) for k in self.keypathh])

    @classmethod
    def rootctx(cls: type[Ctx], root: JObject, ctxcfg: CtxCfg,
                value: Any = None) -> Ctx:
        fdef = types.objof(root.__class__).fdef
        fdef._cdef = root.__class__.cdef
        return Ctx(root=root, owner=root, parent=root, holder=None,
                   val=value if value is not None else root,
                   original=root, ctxcfg=ctxcfg, keypatho=[], keypathr=[],
                   keypathp=[], keypathh=[], fdef=fdef,
                   operator=root._operator, mgraph=MGraph(), idchain=[])

    def nval(self: Ctx, newval: Any) -> Ctx:
        return Ctx(root=self.root, owner=self.owner, parent=self.parent,
                   holder=self.holder, val=newval, original=self.original,
                   ctxcfg=self.ctxcfg, keypatho=self.keypatho,
                   keypathr=self.keypathr, keypathp=self.keypathp,
                   keypathh=self.keypathh, fdef=self.fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain)

    def nextv(self: Ctx, val: Any, key: str | int, fdef: Fdef) -> Ctx:
        return Ctx(root=self.root, owner=self.owner, parent=self.parent,
                   holder=self.holder, val=val, original=None,
                   ctxcfg=self.ctxcfg, keypatho=[*self.keypatho, key],
                   keypathr=[*self.keypathr, key],
                   keypathp=[*self.keypathp, key],
                   keypathh=[*self.keypathh, key], fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain)

    def nexto(self: Ctx, val: Any, key: str | int, fdef: Fdef) -> Ctx:
        return Ctx(root=self.root, owner=val, parent=val, holder=self.owner,
                   val=val, original=None, ctxcfg=self.ctxcfg, keypatho=[],
                   keypathr=[*self.keypathr, key], keypathp=[],
                   keypathh=[key], fdef=fdef, operator=self.operator,
                   mgraph=self.mgraph, idchain=self.idchain)

    def nextvc(self: Ctx, val: Any, key: str | int, fdef: Fdef, c: str) -> Ctx:
        return Ctx(root=self.root, owner=self.owner, parent=self.parent,
                   holder=self.holder, val=val, original=None,
                   ctxcfg=self.ctxcfg, keypatho=[*self.keypatho, key],
                   keypathr=[*self.keypathr, key],
                   keypathp=[*self.keypathp, key],
                   keypathh=[*self.keypathh, key], fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=[*self.idchain, c])

    def nextoc(self: Ctx, val: Any, key: str | int, fdef: Fdef, c: str) -> Ctx:
        return Ctx(root=self.root, owner=val, parent=val, holder=self.owner,
                   val=val, original=None, ctxcfg=self.ctxcfg,
                   keypatho=[], keypathr=[*self.keypathr, key],
                   keypathp=[], keypathh=[key], fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=[*self.idchain, c])

    def nextvo(self: Ctx, val: Any, key: str | int, fdef: Fdef, o: JObject) -> Ctx:
        return Ctx(root=self.root, owner=o, parent=self.parent,
                   holder=self.holder, val=val, original=None,
                   ctxcfg=self.ctxcfg, keypatho=[*self.keypatho, key],
                   keypathr=[*self.keypathr, key],
                   keypathp=[*self.keypathp, key],
                   keypathh=[*self.keypathh, key], fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain)

    def colval(self: Ctx, val: Any, key: str | int, fdef: Fdef, p: Any) -> Ctx:
        return Ctx(root=self.root, owner=self.owner, parent=p,
                   holder=self.holder,
                   val=val, original=None, ctxcfg=self.ctxcfg,
                   keypatho=[*self.keypatho, key],
                   keypathr=[*self.keypathr, key],
                   keypathp=[key], keypathh=[*self.keypathh, key], fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain)

    def default(self: Ctx, owner: JObject, key: str | int, fdef: Fdef) -> Ctx:
        return Ctx(root=self.root, owner=owner, parent=owner,
                   holder=self.holder, val=None,
                   original=None, ctxcfg=self.ctxcfg,
                   keypatho=[*self.keypatho, key],
                   keypathr=[*self.keypathr, key],
                   keypathp=[*self.keypathp, key],
                   keypathh=[*self.keypathh, key], fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain)

    def raise_vexc(self: Ctx, msg: str) -> None:
        """Raise validation error with message.
        """
        raise ValidationException({self.skeypathr: msg}, self.root)

    def raise_mvexc(self: Ctx, msgs: dict[str, str]) -> None:
        raise ValidationException(msgs, self.root)
