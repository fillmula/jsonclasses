"""This is an internal module."""
from __future__ import annotations
from typing import Any, Optional, Union, TYPE_CHECKING
from enum import Enum
from dataclasses import dataclass
if TYPE_CHECKING:
    from .types import Types


class FieldType(Enum):
    """An Enum class represents JSON Class field's type.
    """

    STR = 'str'
    INT = 'int'
    FLOAT = 'float'
    BOOL = 'bool'
    DATE = 'date'
    DATETIME = 'datetime'
    LIST = 'list'
    DICT = 'dict'
    SHAPE = 'shape'
    INSTANCE = 'instance'
    ANY = 'any'
    UNION = 'union'


class FieldStorage(Enum):
    """An Enum class represents JSON Class field's storage.
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


@dataclass
class FieldDefinition:  # pylint: disable=too-many-instance-attributes
    """The description of a JSON Class field. It is generated as specifying the
    marks.
    """

    field_type: Optional[FieldType] = None
    field_storage: FieldStorage = FieldStorage.EMBEDDED

    # primary key
    primary: bool = False
    usage: Optional[str] = None

    # database modifiers
    index: bool = False
    unique: bool = False
    required: bool = False

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


# def is_reference_field(field: Field) -> bool:
#     if field.fdesc.field_storage == FieldStorage.LOCAL_KEY:
#         return True
#     if field.fdesc.field_storage == FieldStorage.FOREIGN_KEY:
#         return True
#     return False


# def is_pure_local_fdesc(cori: Union[JSONObject, type[JSONObject]],
#                         fdesc: FieldDefinition) -> bool:
#     if fdesc.field_storage == FieldStorage.LOCAL_KEY:
#         return False
#     if fdesc.field_storage == FieldStorage.FOREIGN_KEY:
#         return False
#     if fdesc.field_type == FieldType.LIST:
#         item_type = resolve_types(fdesc.raw_item_types, cori)
#         return is_pure_local_fdesc(cori, item_type.fdesc)
#     if fdesc.field_type == FieldType.DICT:
#         item_type = resolve_types(fdesc.raw_item_types, cori)
#         return is_pure_local_fdesc(cori, item_type.fdesc)
#     return True


# def is_pure_local_field(cori: Union[JSONObject, type[JSONObject]],
#                         field: Field) -> bool:
#     return is_pure_local_fdesc(cori, field.fdesc)


# def is_embedded_instance_field(cori: Union[JSONObject, type[JSONObject]],
#                                field: Field) -> bool:
#     from .json_object import JSONObject
#     if field.fdesc.field_type == FieldType.INSTANCE:
#         return True
#     if field.fdesc.field_type == FieldType.LIST:
#         if isinstance(cori, JSONObject):
#             cori = cori.__class__
#         item_types = resolve_types(field.fdesc.raw_item_types,
#                                    cast(type[JSONObject], cori))
#         if item_types.fdesc.field_type == FieldType.INSTANCE:
#             return True
#     return False
