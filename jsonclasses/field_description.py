"""This module contains `FieldDescription`. This is an internal module."""
from __future__ import annotations
from typing import Optional, Any, Dict
from enum import Enum
from dataclasses import dataclass
from copy import deepcopy


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

    def copy(self) -> FieldDescription:
        """This method copies the field description itself and returns a brand new
        copy.
        """
        return deepcopy(self)
