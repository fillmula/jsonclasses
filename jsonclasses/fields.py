"""This is an internal module."""
from __future__ import annotations
from typing import (Any, NamedTuple, Optional, Union, TypeVar, cast,
                    TYPE_CHECKING)
from enum import Enum
from dataclasses import (dataclass, fields as dataclass_fields,
                         Field as DataclassField)
from inflection import camelize
from .types_resolver import resolve_types, to_types
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
class FieldDescription():  # pylint: disable=too-many-instance-attributes
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
    instance_types: Optional[Union[Types, str, type[JSONObject]]] = None

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


class Field(NamedTuple):
    """A JSON Class field.
    """

    field_name: str
    json_field_name: str
    db_field_name: str
    field_types: Types
    assigned_default_value: Any
    fdesc: FieldDescription
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


def get_fields(
    class_or_instance: Union[JSONObject, type[JSONObject]]
) -> list[Field]:
    """Iterate through a JSON Class or JSON Class instance's fields."""
    from .types import Types
    from .json_object import JSONObject
    from .class_graph import class_graph_map
    if isinstance(class_or_instance, JSONObject):
        cls = class_or_instance.__class__
        config = cls.config
    elif issubclass(class_or_instance, JSONObject):
        cls = class_or_instance
        config = class_or_instance.config
    else:
        raise ValueError('wrong argument passed to fields')
    graph = class_graph_map.graph(cls.config.class_graph)
    if graph.get_fields(cls) is not None:
        return graph.get_fields(cls)
    list_fields = []
    dict_fields = {}
    for field in dataclass_fields(class_or_instance):
        field_name = field.name
        json_field_name = camelize(field_name, False) if config.camelize_json_keys else field_name
        db_field_name = camelize(field_name, False) if config.camelize_db_keys else field_name
        field_types = dataclass_field_get_types(field, config.linked_class)
        assigned_default_value = None if isinstance(field.default, Types) else field.default
        if field.default == field.default_factory:  # type: ignore
            assigned_default_value = None
        json_object_field = Field(
            field_name=field_name,
            json_field_name=json_field_name,
            db_field_name=db_field_name,
            field_types=field_types,
            assigned_default_value=assigned_default_value,
            fdesc=field_types.fdesc,
            field_validator=field_types.validator)
        list_fields.append(json_object_field)
        dict_fields[field_name] = json_object_field
    graph.set_fields(cls, list_fields)
    graph.set_dict_fields(cls, dict_fields)
    return list_fields


def field(class_or_instance: Union[JSONObject, type[JSONObject]],
          name: str) -> Optional[Field]:
    from .json_object import JSONObject
    from .class_graph import class_graph_map
    if isinstance(class_or_instance, JSONObject):
        cls = class_or_instance.__class__
    elif issubclass(class_or_instance, JSONObject):
        cls = class_or_instance
    else:
        raise ValueError('unexpected argument passed to field')
    graph = class_graph_map.graph(cls.config.class_graph)
    if graph.get_dict_fields(cls) is not None:
        return graph.get_dict_fields(cls).get(name)
    get_fields(cls)
    return graph.get_dict_fields(cls).get(name)


def fdesc_match_class(fdesc: FieldDescription, cls: type[JSONObject]) -> bool:
    if fdesc.field_type == FieldType.LIST:
        item_types = to_types(fdesc.raw_item_types, cls)
        return fdesc_match_class(item_types.fdesc, cls)
    if fdesc.field_type == FieldType.INSTANCE:
        instance_types = to_types(fdesc.instance_types, cls)
        return instance_types.fdesc.instance_types == cls
    return False


def field_match_class(tfield: Field, cls: type[JSONObject]) -> bool:
    return fdesc_match_class(tfield.fdesc, cls)


def other_field(this: Union[JSONObject, type[JSONObject]],
                other: Union[JSONObject, type[JSONObject]],
                tfield: Union[str, Field]) -> Optional[Field]:
    tclass = cast(Any, this if type(this) is type else this.__class__)
    if isinstance(tfield, str):
        tfield = field(this, tfield)
    tfield = cast(Field, tfield)
    if tfield.fdesc.field_storage == FieldStorage.LOCAL_KEY:
        return next((f for f in get_fields(other)
                    if (f.fdesc.foreign_key == tfield.field_name)
                    and (field_match_class(f, tclass))), None)
    if tfield.fdesc.field_storage == FieldStorage.FOREIGN_KEY:
        fk = tfield.fdesc.foreign_key
        return next((f for f in get_fields(other)
                     if (f.field_name == fk)
                     and field_match_class(f, tclass)), None)
    return None


def is_reference_field(field: Field) -> bool:
    if field.fdesc.field_storage == FieldStorage.LOCAL_KEY:
        return True
    if field.fdesc.field_storage == FieldStorage.FOREIGN_KEY:
        return True
    return False


def is_pure_local_fdesc(cori: Union[JSONObject, type[JSONObject]],
                        fdesc: FieldDescription) -> bool:
    if fdesc.field_storage == FieldStorage.LOCAL_KEY:
        return False
    if fdesc.field_storage == FieldStorage.FOREIGN_KEY:
        return False
    if fdesc.field_type == FieldType.LIST:
        item_type = resolve_types(fdesc.raw_item_types, cori)
        return is_pure_local_fdesc(cori, item_type.fdesc)
    if fdesc.field_type == FieldType.DICT:
        item_type = resolve_types(fdesc.raw_item_types, cori)
        return is_pure_local_fdesc(cori, item_type.fdesc)
    return True


def is_pure_local_field(cori: Union[JSONObject, type[JSONObject]],
                        field: Field) -> bool:
    return is_pure_local_fdesc(cori, field.fdesc)


def is_embedded_instance_field(cori: Union[JSONObject, type[JSONObject]],
                               field: Field) -> bool:
    from .json_object import JSONObject
    if field.fdesc.field_type == FieldType.INSTANCE:
        return True
    if field.fdesc.field_type == FieldType.LIST:
        if isinstance(cori, JSONObject):
            cori = cori.__class__
        item_types = resolve_types(field.fdesc.raw_item_types,
                                   cast(type[JSONObject], cori))
        if item_types.fdesc.field_type == FieldType.INSTANCE:
            return True
    return False


def created_at_field(
        cori: Union[JSONObject, type[JSONObject]]) -> Optional[Field]:
    tfields = get_fields(cori)
    return next((f for f in tfields if f.fdesc.usage == 'created_at'), None)


def updated_at_field(
        cori: Union[JSONObject, type[JSONObject]]) -> Optional[Field]:
    tfields = get_fields(cori)
    return next((f for f in tfields if f.fdesc.usage == 'updated_at'), None)


def deleted_at_field(
        cori: Union[JSONObject, type[JSONObject]]) -> Optional[Field]:
    tfields = get_fields(cori)
    return next((f for f in tfields if f.fdesc.usage == 'deleted_at'), None)
