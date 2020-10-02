"""This is an internal module."""
from __future__ import annotations
from typing import (Any, NamedTuple, Optional, Dict, Union, TypeVar, List,
                    Type, TYPE_CHECKING)
from enum import Enum
from dataclasses import (dataclass,
                         fields as dataclass_fields,
                         Field as DataclassField)
from inflection import camelize
from .types_resolver import to_types
if TYPE_CHECKING:
    from .types import Types
    from .validators.chained_validator import ChainedValidator
    from .json_object import JSONObject
    T = TypeVar('T', bound=JSONObject)


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
    instance_types: Optional[Union[Types, str, Type[JSONObject]]] = None

    # relationship
    foreign_key: Optional[str] = None
    use_join_table: Optional[bool] = None
    join_table_cls: Optional[Any] = None
    join_table_referrer_key: Optional[str] = None
    join_table_referee_key: Optional[str] = None

    read_rule: ReadRule = ReadRule.UNLIMITED
    write_rule: WriteRule = WriteRule.UNLIMITED

    # collection and collection items null rules
    collection_nullability: Nullability = Nullability.NULLABLE
    item_nullability: Nullability = Nullability.UNDEFINED

    strictness: Strictness = Strictness.UNDEFINED

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


def dataclass_field_get_types(
    field: DataclassField, graph_sibling: Any = None
) -> Types:
    """Get JSON Class types from a dataclass field."""
    from .types import Types
    if isinstance(field.default, Types):
        return field.default
    else:
        return to_types(field.type, graph_sibling)


def fields(
    class_or_instance: Union[JSONObject, Type[JSONObject]]
) -> List[Field]:
    """Iterate through a JSON Class or JSON Class instance's fields."""
    from .types import Types
    from .json_object import JSONObject
    from .config import Config
    if isinstance(class_or_instance, JSONObject):
        config = class_or_instance.__class__.config
    elif issubclass(class_or_instance, JSONObject):
        config = class_or_instance.config
    else:
        config = Config()
    retval = []
    for field in dataclass_fields(class_or_instance):
        field_name = field.name
        json_field_name = camelize(field_name, False) if config.camelize_json_keys else field_name
        db_field_name = camelize(field_name, False) if config.camelize_db_keys else field_name
        field_types = dataclass_field_get_types(field, config.linked_class)
        assigned_default_value = None if isinstance(field.default, Types) else field.default
        if field.default == field.default_factory:  # type: ignore
            assigned_default_value = None
        retval.append(
            Field(field_name=field_name,
                  json_field_name=json_field_name,
                  db_field_name=db_field_name,
                  field_types=field_types,
                  assigned_default_value=assigned_default_value,
                  field_description=field_types.field_description,
                  field_validator=field_types.validator))
    return retval
