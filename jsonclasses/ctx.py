"""This module defines JSON Class context objects."""
from __future__ import annotations
from typing import Any, NamedTuple, Union, Optional, cast, TYPE_CHECKING
from .jconf import JConf
from .types import types
from .mgraph import MGraph
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

    reverse_relationship: Optional[bool] = None
    """On tojson, whether output reverse relationship.
    """

    fill_dest_blanks: Optional[bool] = None
    """On set and init, whether fill default fields with None value. This is an
    internal behavior. Do not set this.
    """


class Ctx(NamedTuple):
    root: JObject
    owner: JObject
    parent: list | dict | JObject
    holder: Optional[JObject]
    val: Any
    original: Any
    ctxcfg: CtxCfg
    keypathr: list[str | int]
    fkeypathr: list[str | int]
    keypatho: list[str | int]
    fkeypatho: list[str | int]
    keypathp: list[str | int]
    fkeypathp: list[str | int]
    keypathh: list[str | int]
    fkeypathh: list[str | int]
    fdef: Fdef
    operator: Any
    mgraph: MGraph = MGraph()
    idchain: list[str] = []
    passin: Optional[Any] = None

    @property
    def cdefroot(self: Ctx) -> Cdef:
        return self.root.__class__.cdef

    @property
    def cdefowner(self: Ctx) -> Cdef:
        return self.owner.__class__.cdef

    @property
    def cdefholder(self: Ctx) -> Cdef:
        return cast(JObject, self.holder).__class__.cdef

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

    @property
    def sfkeypathr(self: Ctx) -> str:
        return '.'.join([str(k) for k in self.fkeypathr])

    @property
    def sfkeypatho(self: Ctx) -> str:
        return '.'.join([str(k) for k in self.fkeypatho])

    @property
    def sfkeypathp(self: Ctx) -> str:
        return '.'.join([str(k) for k in self.fkeypathp])

    @property
    def sfkeypathh(self: Ctx) -> str:
        return '.'.join([str(k) for k in self.fkeypathh])

    @classmethod
    def rootctx(cls: type[Ctx], root: JObject, ctxcfg: CtxCfg,
                value: Any = None) -> Ctx:
        fdef = types.objof(root.__class__).fdef
        fdef._cdef = root.__class__.cdef
        return Ctx(root=root, owner=root, parent=root, holder=None,
                   val=value if value is not None else root,
                   original=root, ctxcfg=ctxcfg, keypatho=[], fkeypatho=[],
                   keypathr=[], fkeypathr=[], keypathp=[], fkeypathp=[],
                   keypathh=[], fkeypathh=[], fdef=fdef,
                   operator=root._operator, mgraph=MGraph(), idchain=[])

    @classmethod
    def rootctxp(cls: type[Ctx], root: JObject, key: str, val: Any, passin: Any) -> Ctx:
        fdef = types.objof(root.__class__).fdef
        fdef._cdef = root.__class__.cdef
        ekey = root.__class__.cdef.jconf.key_encoding_strategy(key)
        return Ctx(root=root, owner=root, parent=root, holder=None, val=val,
                   original=root, ctxcfg=CtxCfg(),
                   keypatho=[key], fkeypatho=[ekey],
                   keypathr=[key], fkeypathr=[ekey],
                   keypathp=[key], fkeypathp=[ekey],
                   keypathh=[key], fkeypathh=[ekey],
                   fdef=fdef,
                   operator=root._operator, mgraph=MGraph(), idchain=[],
                   passin=passin)

    def alterfdef(self: Ctx, fdef: Fdef) -> Ctx:
        return Ctx(root=self.root, owner=self.owner, parent=self.parent, holder=self.holder,
                   val=self.val,
                   original=self.original, ctxcfg=self.ctxcfg, keypatho=self.keypatho, fkeypatho=self.fkeypatho,
                   keypathr=self.keypathr, fkeypathr=self.fkeypathr, keypathp=self.keypathp, fkeypathp=self.fkeypathp,
                   keypathh=self.keypathh, fkeypathh=self.fkeypathh, fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph, idchain=self.idchain)

    def nval(self: Ctx, newval: Any) -> Ctx:
        return Ctx(root=self.root, owner=self.owner, parent=self.parent,
                   holder=self.holder, val=newval, original=self.original,
                   ctxcfg=self.ctxcfg,
                   keypatho=self.keypatho, fkeypatho=self.fkeypatho,
                   keypathr=self.keypathr, fkeypathr=self.fkeypathr,
                   keypathp=self.keypathp, fkeypathp=self.fkeypathp,
                   keypathh=self.keypathh, fkeypathh=self.fkeypathh,
                   fdef=self.fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain, passin=self.passin)

    def nextv(self: Ctx, val: Any, key: str | int, fdef: Fdef) -> Ctx:
        ekey = self.owner.__class__.cdef.jconf.key_encoding_strategy(key)
        return Ctx(root=self.root, owner=self.owner, parent=self.parent,
                   holder=self.holder, val=val, original=None,
                   ctxcfg=self.ctxcfg,
                   keypatho=[*self.keypatho, key],
                   fkeypatho=[*self.fkeypatho, ekey],
                   keypathr=[*self.keypathr, key],
                   fkeypathr=[*self.fkeypathr, ekey],
                   keypathp=[*self.keypathp, key],
                   fkeypathp=[*self.fkeypathp, ekey],
                   keypathh=[*self.keypathh, key],
                   fkeypathh=[*self.fkeypathh, ekey],
                   fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain, passin=self.passin)

    def nexto(self: Ctx, val: Any, key: str | int, fdef: Fdef) -> Ctx:
        ekey = self.owner.__class__.cdef.jconf.key_encoding_strategy(key)
        return Ctx(root=self.root, owner=val, parent=val, holder=self.owner,
                   val=val, original=None, ctxcfg=self.ctxcfg, keypatho=[],
                   fkeypatho=[],
                   keypathr=[*self.keypathr, key],
                   fkeypathr=[*self.fkeypathr, ekey],
                   keypathp=[], fkeypathp=[],
                   keypathh=[key], fkeypathh=[ekey], fdef=fdef,
                   operator=self.operator,
                   mgraph=self.mgraph, idchain=self.idchain,
                   passin=self.passin)

    def nextvc(self: Ctx, val: Any, key: str | int, fdef: Fdef, c: str) -> Ctx:
        ekey = self.owner.__class__.cdef.jconf.key_encoding_strategy(key)
        return Ctx(root=self.root, owner=self.owner, parent=self.parent,
                   holder=self.holder, val=val, original=None,
                   ctxcfg=self.ctxcfg,
                   keypatho=[*self.keypatho, key],
                   fkeypatho=[*self.fkeypatho, ekey],
                   keypathr=[*self.keypathr, key],
                   fkeypathr=[*self.fkeypathr, ekey],
                   keypathp=[*self.keypathp, key],
                   fkeypathp=[*self.fkeypathp, ekey],
                   keypathh=[*self.keypathh, key],
                   fkeypathh=[*self.fkeypathh, ekey],
                   fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=[*self.idchain, c], passin=self.passin)

    def nextoc(self: Ctx, val: Any, key: str | int, fdef: Fdef, c: str) -> Ctx:
        ekey = self.owner.__class__.cdef.jconf.key_encoding_strategy(key)
        return Ctx(root=self.root, owner=val, parent=val, holder=self.owner,
                   val=val, original=None, ctxcfg=self.ctxcfg,
                   keypatho=[],
                   fkeypatho=[],
                   keypathr=[*self.keypathr, key],
                   fkeypathr=[*self.fkeypathr, ekey],
                   keypathp=[],
                   fkeypathp=[],
                   keypathh=[key],
                   fkeypathh=[ekey],
                   fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=[*self.idchain, c], passin=self.passin)

    def nextvo(self: Ctx, val: Any, key: str | int, fdef: Fdef, o: JObject) -> Ctx:
        ekey = self.owner.__class__.cdef.jconf.key_encoding_strategy(key)
        return Ctx(root=self.root, owner=o, parent=self.parent,
                   holder=self.holder, val=val, original=None,
                   ctxcfg=self.ctxcfg,
                   keypatho=[*self.keypatho, key],
                   fkeypatho=[*self.fkeypatho, ekey],
                   keypathr=[*self.keypathr, key],
                   fkeypathr=[*self.fkeypathr, ekey],
                   keypathp=[*self.keypathp, key],
                   fkeypathp=[*self.fkeypathp, ekey],
                   keypathh=[*self.keypathh, key],
                   fkeypathh=[*self.fkeypathh, ekey],
                   fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain, passin=self.passin)

    def colval(self: Ctx, val: Any, key: str | int, fdef: Fdef, p: Any) -> Ctx:
        return Ctx(root=self.root, owner=self.owner, parent=p,
                   holder=self.holder,
                   val=val, original=None, ctxcfg=self.ctxcfg,
                   keypatho=[*self.keypatho, key],
                   fkeypatho=[*self.fkeypatho, key],
                   keypathr=[*self.keypathr, key],
                   fkeypathr=[*self.fkeypathr, key],
                   keypathp=[key],
                   fkeypathp=[*self.fkeypathp, key],
                   keypathh=[*self.keypathh, key],
                   fkeypathh=[*self.fkeypathh, key],
                   fdef=fdef,
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain, passin=self.passin)

    def default(self: Ctx, owner: JObject, key: str | int, fdef: Fdef) -> Ctx:
        ekey = self.owner.__class__.cdef.jconf.key_encoding_strategy(key)
        return Ctx(root=self.root, owner=owner, parent=owner,
                   holder=self.holder, val=None,
                   original=None, ctxcfg=self.ctxcfg,
                   keypatho=[*self.keypatho, key],
                   fkeypatho=[*self.fkeypatho, ekey],
                   keypathr=[*self.keypathr, key],
                   fkeypathr=[*self.fkeypathr, ekey],
                   keypathp=[*self.keypathp, key],
                   fkeypathp=[*self.fkeypathp, ekey],
                   keypathh=[*self.keypathh, key], fdef=fdef,
                   fkeypathh=[*self.fkeypathh, ekey],
                   operator=self.operator, mgraph=self.mgraph,
                   idchain=self.idchain, passin=self.passin)

    def raise_vexc(self: Ctx, msg: str) -> None:
        """Raise validation error with message.
        """
        raise ValidationException({self.sfkeypathr: msg}, self.root)

    def raise_mvexc(self: Ctx, msgs: dict[str, str]) -> None:
        raise ValidationException(msgs, self.root)
