"""This is an internal module."""
from __future__ import annotations
from typing import cast, Any, Callable, Optional, TYPE_CHECKING
from enum import Enum, Flag
from .rtypes import rnamedtypes, rtypes
from .isjsonclass import isjsonclass
from .jobject import JObject
if TYPE_CHECKING:
    from .types import Types
    from .cdef import Cdef


class FType(Enum):
    """Defined field types of jsonclass fields.
    """

    STR = 'str'
    INT = 'int'
    FLOAT = 'float'
    BOOL = 'bool'
    DATE = 'date'
    DATETIME = 'datetime'
    ENUM = 'enum'
    LIST = 'list'
    DICT = 'dict'
    INSTANCE = 'instance'
    ANY = 'any'
    UNION = 'union'


class FStore(Enum):
    """Defined field storage types of jsonclass fields.
    """

    EMBEDDED = 'embedded'
    LOCAL_KEY = 'local_key'
    FOREIGN_KEY = 'foreign_key'
    CALCULATED = 'calculated'
    TEMP = 'temp'


class ReadRule(Enum):
    """An Enum class represents JSON Class field's read rule.
    """

    UNLIMITED = 'unlimited'
    NO_READ = 'no_read'


class WriteRule(Enum):
    """An Enum class represents JSON Class field's write rule.
    """

    UNLIMITED = 'unlimited'
    NO_WRITE = 'no_write'
    WRITE_ONCE = 'write_once'
    WRITE_NONNULL = 'write_nonnull'


class Nullability(Enum):
    """An Enum class represents JSON Class field's nullability. This only works
    for collection types and their inner item types.
    """

    UNDEFINED = 'undefined'
    NULLABLE = 'nullable'
    NONNULL = 'nonnull'


class Strictness(Enum):
    """Instance's strictness.
    """

    UNDEFINED = 'undefined'
    STRICT = 'strict'
    UNSTRICT = 'unstrict'


class DeleteRule(Enum):
    """The delete rule of a relationship.
    """

    NULLIFY = 'nullify'
    CASCADE = 'cascade'
    DENY = 'deny'


class EnumInput(Flag):
    NAME = 1
    VALUE = 2
    LOWERCASE_NAME = 4
    NAME_VALUE = NAME | VALUE
    ANYCASE_NAME = NAME | LOWERCASE_NAME
    LOWERCASE_NAME_VALUE = LOWERCASE_NAME | VALUE
    ALL = NAME | VALUE | LOWERCASE_NAME


class EnumOutput(Enum):
    NAME = 'name'
    VALUE = 'value'
    LOWERCASE_NAME = 'lowercase_name'


class Queryability(Enum):
    QUERYABLE = 'queryable'
    UNQUERYABLE = 'unqueryable'


class CopyBehavior(Enum):
    COPY = "copy"
    NOCOPY = "nocopy"


class Fdef:
    """The description of a JSONClass field. Some type markers annotate on
    this definition.
    """

    def __init__(self: Fdef) -> None:
        self._cdef: Optional[Cdef] = None
        self._unresolved: bool = False
        self._unresolved_name: Optional[str] = None
        self._ftype: Optional[FType] = None
        self._fstore: FStore = FStore.EMBEDDED
        self._getter: Types | Callable | None = None
        self._setter: Types | Callable | None = None
        self._primary: bool = False
        self._index: bool = False
        self._cindex: bool = False
        self._cindex_names: list[str] = []
        self._cunique: bool = False
        self._cunique_names: list[str] = []
        self._unique: bool = False
        self._required: bool = False
        self._raw_enum_class: Optional[type[Enum] | str] = None
        self._enum_class: Optional[type[Enum]] = None
        self._enum_input: Optional[EnumInput] = None
        self._enum_output: Optional[EnumOutput] = None
        self._raw_union_types: Optional[list[Types]] = None
        self._raw_item_types: Optional[Any] = None
        self._raw_inst_types: Optional[str | type[JObject]] = None
        self._resolved_union_types: Optional[list[Types]] = None
        self._resolved_item_types: Optional[Types] = None
        self._inst_cls: Optional[type[JObject]] = None
        self._force_set_on_save: bool = False
        self._foreign_key: Optional[str] = None
        self._use_join_table: Optional[bool] = None
        self._join_table_cls: Optional[Any] = None
        self._join_table_referrer_key: Optional[str] = None
        self._join_table_referee_key: Optional[str] = None
        self._delete_rule: Optional[DeleteRule] = None
        self._read_rule: ReadRule = ReadRule.UNLIMITED
        self._write_rule: WriteRule = WriteRule.UNLIMITED
        self._collection_nullability: Nullability = Nullability.NULLABLE
        self._item_nullability: Nullability = Nullability.UNDEFINED
        self._strictness: Strictness = Strictness.UNDEFINED
        self._has_eager_modifier: bool = False
        self._has_reset_modifier: bool = False
        self._has_preserialize_modifier: bool = False
        self._requires_operator_assign: bool = False
        self._operator_assign_transformer: Optional[Callable] = None
        self._queryability: Optional[Queryability] = None
        self._copy_behavior: Optional[CopyBehavior] = None
        self._auth_identity: bool = False
        self._auth_by: bool = False
        self._auth_by_checker: Optional[Types] = None

    @property
    def cdef(self: Fdef) -> Cdef:
        """The class definition which owns this field.
        """
        from .cdef import Cdef
        return cast(Cdef, self._cdef)

    @property
    def ftype(self: Fdef) -> FType:
        """The field's type.
        """
        self._resolve_if_needed()
        return cast(FType, self._ftype)

    @property
    def fstore(self: Fdef) -> FStore:
        """The field's storage.
        """
        self._resolve_if_needed()
        return self._fstore

    @property
    def getter(self: Fdef) -> Types | Callable | None:
        """The calculated field's getter.
        """
        self._resolve_if_needed()
        return self._getter

    @property
    def setter(self: Fdef) -> Types | Callable | None:
        """The calculated field's setter.
        """
        self._resolve_if_needed()
        return self._setter

    # primary key

    @property
    def primary(self: Fdef) -> bool:
        """Whether this field is a primary field. A class can only has one
        primary field.
        """
        self._resolve_if_needed()
        return self._primary

    # database modifiers

    @property
    def index(self: Fdef) -> bool:
        """Whether perform single database index on this field. This is marked
        for ORM implementers.
        """
        self._resolve_if_needed()
        return self._index

    @property
    def cindex(self: Fdef) -> bool:
        """Whether perform compound database index on this field. This is
        marked for ORM implementers.
        """
        self._resolve_if_needed()
        return self._cindex

    @property
    def cindex_names(self: Fdef) -> list[str]:
        """The compound index name for this index field.
        """
        self._resolve_if_needed()
        return self._cindex_names

    @property
    def unique(self: Fdef) -> bool:
        """Whether this field's value is unique. This is marked for ORM
        implementers.
        """
        self._resolve_if_needed()
        return self._unique

    @property
    def cunique(self: Fdef) -> bool:
        """Whether perform compound database index on this field. This is
        marked for ORM implementers.
        """
        self._resolve_if_needed()
        return self._cunique

    @property
    def cunique_names(self: Fdef) -> list[str]:
        """The compound index name for this index field.
        """
        self._resolve_if_needed()
        return self._cunique_names

    @property
    def required(self: Fdef) -> bool:
        """Whether this field is required. This is marked for ORM
        implementers.
        """
        self._resolve_if_needed()
        return self._required

    # enum marks

    @property
    def raw_enum_class(self: Fdef) -> Optional[type[Enum] | str]:
        """The raw enum class.
        """
        self._resolve_if_needed()
        return self._raw_enum_class

    @property
    def enum_class(self: Fdef) -> type[Enum]:
        """The class of the enum.
        """
        self._resolve_if_needed()
        if self._enum_class is not None:
            return self._enum_class
        if isinstance(self._raw_enum_class, str):
            ecls = self.cdef.jconf.cgraph.fetch_enum(self._raw_enum_class)
            self._enum_class = ecls
        else:
            self._enum_class = self._raw_enum_class
        return cast(type[Enum], self._enum_class)

    @property
    def enum_input(self: Fdef) -> Optional[EnumInput]:
        """The allowed input types of this enum class.
        """
        self._resolve_if_needed()
        return self._enum_input

    @property
    def enum_output(self: Fdef) -> Optional[EnumOutput]:
        """The output type of this enum class.
        """
        self._resolve_if_needed()
        return self._enum_output

    @property
    def raw_union_types(self: Fdef) -> Optional[list[Types]]:
        """The raw union types of this union field.
        """
        self._resolve_if_needed()
        return self._raw_union_types

    # subtypes

    @property
    def raw_item_types(self: Fdef) -> Optional[Any]:
        """The raw item types of this collection field.
        """
        self._resolve_if_needed()
        return self._raw_item_types

    @property
    def item_types(self: Fdef) -> Types:
        """The item types of this collection field.
        """
        from .types import Types
        self._resolve_if_needed()
        if self._raw_item_types is None:
            return cast(Types, None)
        if self._resolved_item_types is not None:
            return self._resolved_item_types
        self._resolved_item_types = rtypes(self.raw_item_types)
        self._resolved_item_types.fdef._cdef = self.cdef
        self._resolved_item_types = rnamedtypes(
            self._resolved_item_types,
            self.cdef.jconf.cgraph,
            self.cdef.name)
        if self._resolved_item_types.fdef.item_nullability == Nullability.UNDEFINED:
            self._resolved_item_types = self._resolved_item_types.required
        return self._resolved_item_types

    @property
    def raw_inst_types(self: Fdef) -> Optional[str | type[JObject]]:
        """The raw instance types of this instance field.
        """
        self._resolve_if_needed()
        return self._raw_inst_types

    @property
    def inst_cls(self: Fdef) -> Optional[type[JObject]]:
        """The instance class of this field.
        """
        self._resolve_if_needed()
        if self._inst_cls:
            return self._inst_cls
        if self._raw_inst_types is None:
            return None
        if isjsonclass(self._raw_inst_types):
            self._inst_cls = cast(type[JObject], self._raw_inst_types)
        cgraph = self.cdef.jconf.cgraph
        inst_cls = cgraph.fetch(self._raw_inst_types).cls
        self._inst_cls = inst_cls
        return self._inst_cls

    @property
    def force_set_on_save(self: Fdef) -> bool:
        """Whether force set on save."""
        self._resolve_if_needed()
        return self._force_set_on_save

    # relationship

    @property
    def foreign_key(self: Fdef) -> Optional[str]:
        """The foreign key of the relationship.
        """
        self._resolve_if_needed()
        return self._foreign_key

    @property
    def use_join_table(self: Fdef) -> Optional[bool]:
        """Whether this reference uses join table.
        """
        self._resolve_if_needed()
        return self._use_join_table

    @property
    def join_table_cls(self: Fdef) -> Optional[Any]:
        """The join table class of the relationship.
        """
        self._resolve_if_needed()
        return self._join_table_cls

    @property
    def join_table_referrer_key(self: Fdef) -> Optional[str]:
        """The referrer key of the join table.
        """
        self._resolve_if_needed()
        return self._join_table_referrer_key

    @property
    def join_table_referee_key(self: Fdef) -> Optional[str]:
        """The referee key of the join table.
        """
        self._resolve_if_needed()
        return self._join_table_referee_key

    @property
    def delete_rule(self: Fdef) -> Optional[DeleteRule]:
        """The delete rule of this relationship.
        """
        self._resolve_if_needed()
        return self._delete_rule

    # read write rule

    @property
    def read_rule(self: Fdef) -> ReadRule:
        """The read rule of this field.
        """
        self._resolve_if_needed()
        return self._read_rule

    @property
    def write_rule(self: Fdef) -> WriteRule:
        """The write rule of this field.
        """
        self._resolve_if_needed()
        return self._write_rule

    # collection and collection items null rules

    @property
    def collection_nullability(self: Fdef) -> Nullability:
        """The collection nullability of this field.
        """
        self._resolve_if_needed()
        return self._collection_nullability

    @property
    def item_nullability(self: Fdef) -> Nullability:
        """The item nullability of this field.
        """
        self._resolve_if_needed()
        return self._item_nullability

    @property
    def strictness(self: Fdef) -> Strictness:
        """The strictness of this instance field.
        """
        self._resolve_if_needed()
        return self._strictness

    # special modifier marks

    @property
    def has_eager_modifier(self: Fdef) -> bool:
        """Whether there is at least an eager modifier in the chain.
        """
        self._resolve_if_needed()
        return self._has_eager_modifier

    @property
    def has_reset_modifier(self: Fdef) -> bool:
        """Whether there is at least an reset modifier in the chain.
        """
        self._resolve_if_needed()
        return self._has_reset_modifier

    @property
    def has_preserialize_modifier(self: Fdef) -> bool:
        """Whether there is at least a preserialize modifier in the chain.
        """
        self._resolve_if_needed()
        return self._has_preserialize_modifier

    # operator

    @property
    def requires_operator_assign(self: Fdef) -> bool:
        """Whether this field requires an operator assigned.
        """
        self._resolve_if_needed()
        return self._requires_operator_assign

    @property
    def operator_assign_transformer(self: Fdef) -> Optional[Callable]:
        """The operator assign transformer of this field.
        """
        self._resolve_if_needed()
        return self._operator_assign_transformer

    @property
    def queryability(self: Fdef) -> Queryability:
        """The queryability of this field.
        """
        self._resolve_if_needed()
        return self._queryability or Queryability.QUERYABLE

    @property
    def copy_behavior(self: Fdef) -> CopyBehavior:
        """The copy behavior of this field.
        """
        self._resolve_if_needed()
        return self._copy_behavior or CopyBehavior.COPY

    @property
    def auth_identity(self: Fdef) -> bool:
        """Whether this field is authorization identity.
        """
        self._resolve_if_needed()
        return self._auth_identity

    @property
    def auth_by(self: Fdef) -> bool:
        """Whether this field is authorization checker.
        """
        self._resolve_if_needed()
        return self._auth_by

    @property
    def auth_by_checker(self: Fdef) -> Types:
        """The auth by checker of this field.
        """
        from .types import Types
        self._resolve_if_needed()
        return cast(Types, self._auth_by_checker)

    # old reference properties

    @property
    def is_ref(self: Fdef) -> bool:
        self._resolve_if_needed()
        if self.fstore in \
                [FStore.LOCAL_KEY, FStore.FOREIGN_KEY]:
            return True
        return False

    @property
    def is_inst(self: Fdef) -> bool:
        self._resolve_if_needed()
        if self.ftype == FType.INSTANCE:
            return True
        if self.ftype == FType.LIST:
            if self.item_types.fdef.ftype == FType.INSTANCE:
                return True
        return False

    @property
    def has_linked(self: Fdef) -> bool:
        self._resolve_if_needed()
        if self.fstore == FStore.LOCAL_KEY:
            return True
        if self.fstore == FStore.FOREIGN_KEY:
            return True
        if self.ftype == FType.LIST:
            return self.item_types.fdef.has_linked
        return False

    def _resolve_if_needed(self: Fdef) -> None:
        if self._unresolved:
            # resolve
            self._resolve()
            self._unresolved = False
            self._unresolved_name = None

    def _resolve(self: Fdef) -> None:
        self.cdef._resolve_ref_types_if_needed()

    def __str__(self):
        return '<Fdef: ' + str(vars(self)) + '>'
