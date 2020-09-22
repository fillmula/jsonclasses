"""This is an internal module."""
from __future__ import annotations
from typing import Any, NamedTuple, Optional, Dict, TYPE_CHECKING
from enum import Enum
from dataclasses import dataclass
if TYPE_CHECKING:
    from .types import Types
    from .validators.chained_validator import ChainedValidator


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


class CollectionNullability(Enum):
    """An Enum class represents JSON Class field's collection nullability. This
    only works for collection types.
    """

    UNDEFINED = 'undefined'
    NULLABLE = 'nullable'


@dataclass
class FieldDescription():  # pylint: disable=too-many-instance-attributes
    """The description of a JSON Class field. It is generated as specifying the
    marks.
    """

    field_type: Optional[FieldType] = None
    field_storage: FieldStorage = FieldStorage.EMBEDDED

    index: bool = False
    unique: bool = False
    required: bool = False

    # collection marks
    list_item_types: Optional[Any] = None
    dict_item_types: Optional[Any] = None
    shape_types: Optional[Dict[str, Any]] = None

    # instance mark
    instance_types: Optional[Any] = None

    # relationship
    foreign_key: Optional[str] = None
    use_join_table: Optional[bool] = None
    join_table_cls: Optional[Any] = None
    join_table_referrer_key: Optional[str] = None
    join_table_referee_key: Optional[str] = None

    read_rule: ReadRule = ReadRule.UNLIMITED
    write_rule: WriteRule = WriteRule.UNLIMITED

    collection_nullability: CollectionNullability = CollectionNullability.UNDEFINED

    has_eager_validator: bool = False


class Field(NamedTuple):
    """A JSON Class field.
    """

    field_name: str
    json_field_name: str
    db_field_name: str
    field_types: Types
    assigned_default_value: Any
    field_description: FieldDescription
    field_validator: ChainedValidator
