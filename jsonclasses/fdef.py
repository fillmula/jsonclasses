"""This is an internal module."""
from __future__ import annotations
from typing import cast, Any, Callable, Optional, Union, TYPE_CHECKING
from enum import Enum, Flag
from .rtypes import rtypes
if TYPE_CHECKING:
    from .types import Types
    from .cdef import Cdef


class FieldType(Enum):
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
    SHAPE = 'shape'
    INSTANCE = 'instance'
    ANY = 'any'
    UNION = 'union'


class FieldStorage(Enum):
    """Defined field storage types of jsonclass fields.
    """

    EMBEDDED = 'embedded'
    LOCAL_KEY = 'local_key'
    FOREIGN_KEY = 'foreign_key'


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
    """Instance and shape's strictness.
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


class Fdef:
    """The description of a JSONClass field. Some type markers annotate on
    this definition.
    """

    def __init__(self: Fdef) -> None:
        self._cdef: Optional[Cdef] = None
        self._field_type: Optional[FieldType] = None
        self._field_storage: FieldStorage = FieldStorage.EMBEDDED
        self._primary: bool = False
        self._usage: Optional[str] = None
        self._index: bool = False
        self._unique: bool = False
        self._required: bool = False
        self._enum_class: Optional[Union[type[Enum], str]] = None
        self._enum_input: Optional[EnumInput] = None
        self._enum_output: Optional[EnumOutput] = None
        self._union_types: Optional[list[Types]] = None
        self._raw_item_types: Optional[Any] = None
        self._raw_shape_types: Optional[dict[str, Any]] = None
        self._raw_inst_types: Optional[Union[Types, str, type]] = None
        self._foreign_key: Optional[str] = None
        self._use_join_table: Optional[bool] = None
        self._join_table_cls: Optional[Any] = None
        self._join_table_referrer_key: Optional[str] = None
        self._join_table_referee_key: Optional[str] = None
        self._delete_rule: Optional[DeleteRule] = None
        self._read_rule: ReadRule = ReadRule.UNLIMITED
        self._write_rule: WriteRule = WriteRule.UNLIMITED
        self._is_temp_field: bool = False
        self._collection_nullability: Nullability = Nullability.NULLABLE
        self._item_nullability: Nullability = Nullability.UNDEFINED
        self._strictness: Strictness = Strictness.UNDEFINED
        self._has_eager_validator: bool = False
        self._has_reset_validator: bool = False
        self._has_preserialize_validator: bool = False
        self._requires_operator_assign: bool = False
        self._operator_assign_transformer: Optional[Callable] = None

    @property
    def cdef(self: Fdef) -> Cdef:
        """The class definition which owns this field.
        """
        return cast('Cdef', self._cdef)

    @property
    def field_type(self: Fdef) -> FieldType:
        """The field's type.
        """
        return cast(FieldType, self._field_type)

    @property
    def field_storage(self: Fdef) -> FieldStorage:
        """The field's storage.
        """
        return self._field_storage

    # primary key

    @property
    def primary(self: Fdef) -> bool:
        """Whether this field is a primary field. A class can only has one
        primary field.
        """
        return self._primary

    @property
    def usage(self: Fdef) -> Optional[str]:
        """The usage of this field.
        """
        return self._usage

    # database modifiers

    @property
    def index(self: Fdef) -> bool:
        """Whether perform database index on this field. This is marked for
        ORM implementers.
        """
        return self._index

    @property
    def unique(self: Fdef) -> bool:
        """Whether this field's value is unique. This is marked for ORM
        implementers.
        """
        return self._unique

    @property
    def required(self: Fdef) -> bool:
        """Whether this field is required. This is marked for ORM
        implementers.
        """
        return self._required

    # enum marks

    @property # TODO: raw enum class
    def enum_class(self: Fdef) -> Optional[Union[type[Enum], str]]:
        """The class of the enum.
        """
        return self._enum_class

    @property
    def enum_input(self: Fdef) -> Optional[EnumInput]:
        """The allowed input types of this enum class.
        """
        return self._enum_input

    @property
    def enum_output(self: Fdef) -> Optional[EnumOutput]:
        """The output type of this enum class.
        """
        return self._enum_output

    @property
    def raw_union_types(self: Fdef) -> Optional[list[Types]]:
        """The raw union types of this union field.
        """
        return self._union_types

    # subtypes

    @property
    def raw_item_types(self: Fdef) -> Optional[Any]:
        """The raw item types of this collection field.
        """
        return self._raw_item_types

    @property
    def raw_shape_types(self: Fdef) -> Optional[dict[str, Any]]:
        """The raw shape types of this shape field.
        """
        return self._raw_shape_types

    @property
    def raw_inst_types(self: Fdef) -> Optional[Union[Types, str, type]]:
        """The raw instance types of this instance field.
        """
        return self._raw_inst_types

    # relationship

    @property
    def foreign_key(self: Fdef) -> Optional[str]:
        """The foreign key of the relationship.
        """
        return self._foreign_key

    @property
    def use_join_table(self: Fdef) -> Optional[bool]:
        """Whether this reference uses join table.
        """
        return self._use_join_table

    @property
    def join_table_cls(self: Fdef) -> Optional[Any]:
        """The join table class of the relationship.
        """
        return self._join_table_cls

    @property
    def join_table_referrer_key(self: Fdef) -> Optional[str]:
        """The referrer key of the join table.
        """
        return self._join_table_referrer_key

    @property
    def join_table_referee_key(self: Fdef) -> Optional[str]:
        """The referee key of the join table.
        """
        return self._join_table_referee_key

    @property
    def delete_rule(self: Fdef) -> Optional[DeleteRule]:
        """The delete rule of this relationship.
        """
        return self._delete_rule

    # read write rule

    @property
    def read_rule(self: Fdef) -> ReadRule:
        """The read rule of this field.
        """
        return self._read_rule

    @property
    def write_rule(self: Fdef) -> WriteRule:
        """The write rule of this field.
        """
        return self._write_rule

    @property
    def is_temp_field(self: Fdef) -> bool:
        """Whether this field is a temp field.
        """
        return self._is_temp_field

    # collection and collection items null rules

    @property
    def collection_nullability(self: Fdef) -> Nullability:
        """The collection nullability of this field.
        """
        return self._collection_nullability

    @property
    def item_nullability(self: Fdef) -> Nullability:
        """The item nullability of this field.
        """
        return self._item_nullability

    @property
    def strictness(self: Fdef) -> Strictness:
        """The strictness of this shape field.
        """
        return self._strictness

    # special validator marks

    @property
    def has_eager_validator(self: Fdef) -> bool:
        """Whether there is at least an eager validator in the chain.
        """
        return self._has_eager_validator

    @property
    def has_reset_validator(self: Fdef) -> bool:
        """Whether there is at least an reset validator in the chain.
        """
        return self._has_reset_validator

    @property
    def has_preserialize_validator(self: Fdef) -> bool:
        """Whether there is at least a preserialize validator in the chain.
        """
        return self._has_preserialize_validator

    # operator

    @property
    def requires_operator_assign(self: Fdef) -> bool:
        """Whether this field requires an operator assigned.
        """
        return self._requires_operator_assign

    @property
    def operator_assign_transformer(self: Fdef) -> Optional[Callable]:
        """The operator assign transformer of this field.
        """
        return self._operator_assign_transformer

    # old reference properties

    @property
    def is_ref(self: Fdef) -> bool:
        if self.field_storage in \
                [FieldStorage.LOCAL_KEY, FieldStorage.FOREIGN_KEY]:
            return True
        return False

    @property
    def is_inst(self: Fdef) -> bool:
        if self.field_type == FieldType.INSTANCE:
            return True
        if self.field_type == FieldType.LIST:
            item_types = rtypes(
                self.raw_item_types,
                self.cdef.config)
            if item_types.fdef.field_type == FieldType.INSTANCE:
                return True
        return False

    @property
    def has_linked(self: Fdef) -> bool:
        if self.field_storage == FieldStorage.LOCAL_KEY:
            return True
        if self.field_storage == FieldStorage.FOREIGN_KEY:
            return True
        if self.field_type == FieldType.LIST or \
                self.field_type == FieldType.DICT:
            item_type = rtypes(self.raw_item_types, self.cdef.config)
            return item_type.fdef.has_linked
        return False
