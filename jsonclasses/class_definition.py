"""
This module defines `ClassDefinition`. Each JSON class has its own class
definition. The class definition object contains detailed information about how
user defines a JSON class. This is used by the framework to lookup class fields
and class field settings.
"""
from __future__ import annotations
from typing import final, TYPE_CHECKING
from dataclasses import fields, Field
from inflection import camelize
from .jsonclass_field import JSONClassField
if TYPE_CHECKING:
    from .new_config import Config
    from .types import Types


@final
class ClassDefinition:
    """Class definition represents the class definition of JSON classes. Each
    JSON class has its own class definition. The class definition object
    contains detailed information about how user defines a JSON class. This is
    used by the framework to lookup class fields and class field settings.
    """

    def __init__(self: ClassDefinition, class_: type, config: Config) -> None:
        """
        Initialize a new class definition.

        Args:
            class_ (type): The JSON class for which the class definition is \
                created.
            config (Config): The configuration object for the targeted class.
        """
        self._list_fields = []
        self._dict_fields = {}
        for field in fields(class_):
            name = field.name
            if config.camelize_json_keys:
                json_name = camelize(name, False)
            else:
                json_name = name
            if config.camelize_db_keys:
                db_name = camelize(name, False)
            else:
                db_name = name
            types = self._get_types(field, config.linked_class)
            assigned_default_value = None if isinstance(field.default, Types) else field.default
            if field.default == field.default_factory:  # type: ignore
                assigned_default_value = None
            jsonclass_field = JSONClassField(
                name=name,
                json_name==json_name,
                db_name==db_name,
                field_types=field_types,
                assigned_default_value=assigned_default_value,
                fdesc=field_types.fdesc,
                field_validator=field_types.validator)
            self._list_fields.append(jsonclass_field)
            self._dict_fields[name] = jsonclass_field

    def _get_types(self: ClassDefinition,
                   field: Field,
                   config: Config) -> Types:
        """
        Try to fetch the types definition from the field definition. If user
        hasn't define a types definition, an automatically synthesized one is
        returned.
        """
        from .types import Types
        if isinstance(field.default, Types):
            return field.default
        else:
            return to_types(field.type, graph_sibling)
