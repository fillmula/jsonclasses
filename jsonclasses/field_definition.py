"""This is an internal module."""
from __future__ import annotations
from typing import Any, Callable, Optional, Union, TYPE_CHECKING
from enum import Enum, Flag
from dataclasses import dataclass
from .types_resolver import TypesResolver
if TYPE_CHECKING:
    from .types import Types
    from .class_definition import ClassDefinition


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


@dataclass
class FieldDefinition:  # pylint: disable=too-many-instance-attributes
    """The description of a JSON Class field. It is generated as specifying the
    marks.
    """

    class_definition: ClassDefinition = None

    field_type: Optional[FieldType] = None
    field_storage: FieldStorage = FieldStorage.EMBEDDED

    # primary key
    primary: bool = False
    usage: Optional[str] = None

    # database modifiers
    index: bool = False
    unique: bool = False
    required: bool = False

    # enum marks
    enum_class: Optional[Union[type, str]] = None
    enum_input: Optional[EnumInput] = None
    enum_output: Optional[EnumOutput] = None

    # union marks
    union_types: Optional[list[Types]] = None

    # collection marks
    raw_item_types: Optional[Any] = None
    shape_types: Optional[dict[str, Any]] = None

    # instance mark
    instance_types: Optional[Union[Types, str, type]] = None

    # relationship
    foreign_key: Optional[str] = None
    use_join_table: Optional[bool] = None
    join_table_cls: Optional[Any] = None
    join_table_referrer_key: Optional[str] = None
    join_table_referee_key: Optional[str] = None
    delete_rule: Optional[DeleteRule] = None

    read_rule: ReadRule = ReadRule.UNLIMITED
    write_rule: WriteRule = WriteRule.UNLIMITED
    is_temp_field: bool = False

    # collection and collection items null rules
    collection_nullability: Nullability = Nullability.NULLABLE
    item_nullability: Nullability = Nullability.UNDEFINED

    strictness: Strictness = Strictness.UNDEFINED

    has_eager_validator: bool = False
    has_reset_validator: bool = False
    has_preserialize_validator: bool = False

    # operator
    requires_operator_assign: bool = False
    operator_assign_transformer: Optional[Callable] = None

    @property
    def is_ref(self: FieldDefinition) -> bool:
        if self.field_storage in \
                [FieldStorage.LOCAL_KEY, FieldStorage.FOREIGN_KEY]:
            return True
        return False

    @property
    def is_inst(self: FieldDefinition) -> bool:
        if self.field_type == FieldType.INSTANCE:
            return True
        if self.field_type == FieldType.LIST:
            item_types = TypesResolver().resolve_types(
                self.raw_item_types,
                self.class_definition.config)
            if item_types.definition.field_type == FieldType.INSTANCE:
                return True
        return False

    @property
    def has_linked(self: FieldDefinition) -> bool:
        if self.field_storage == FieldStorage.LOCAL_KEY:
            return True
        if self.field_storage == FieldStorage.FOREIGN_KEY:
            return True
        if self.field_type == FieldType.LIST or \
                self.field_type == FieldType.DICT:
            item_type = TypesResolver() \
                .resolve_types(self.raw_item_types,
                               self.class_definition.config)
            return item_type.definition.has_linked
