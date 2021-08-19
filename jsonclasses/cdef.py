"""
This module defines `Cdef`. Each JSON class has its own class
definition. The class definition object contains detailed information about how
user defines a JSON class. This is used by the framework to lookup class fields
and class field settings.
"""
from __future__ import annotations
from typing import Optional, final, cast, TYPE_CHECKING
from dataclasses import fields, Field
from inflection import camelize
from .jfield import JField
from .fdef import Fdef, FieldStorage, FieldType, DeleteRule
from .rtypes import rtypes
from .exceptions import LinkedFieldUnmatchException
if TYPE_CHECKING:
    from .config import Config
    from .types import Types


@final
class Cdef:
    """Class definition represents the class definition of JSON classes. Each
    JSON class has its own class definition. The class definition object
    contains detailed information about how user defines a JSON class. This is
    used by the framework to lookup class fields and class field settings.
    """

    def __init__(self: Cdef, class_: type, config: Config) -> None:
        """
        Initialize a new class definition.

        Args:
            class_ (type): The JSON class for which the class definition is \
                created.
            config (Config): The configuration object for the targeted class.
        """
        from .types import Types
        self._cls: type = class_
        config._cls = class_
        self._name: str = class_.__name__
        self._config: Config = config
        self._list_fields: list[JField] = []
        self._dict_fields: dict[str, JField] = {}
        self._foreign_fields: dict[str, Optional[tuple[Cdef, str]]]\
            = {}
        self._primary_field: Optional[JField] = None
        self._created_at_field: Optional[JField] = None
        self._updated_at_field: Optional[JField] = None
        self._deleted_at_field: Optional[JField] = None
        self._deny_fields: list[JField] = []
        self._nullify_fields: list[JField] = []
        self._cascade_fields: list[JField] = []
        self._field_names: list[str] = []
        self._camelized_field_names: list[str] = []
        self._reference_names: list[str] = []
        self._camelized_reference_names: list[str] = []
        self._assign_operator_fields: list[JField] = []
        for field in fields(class_):
            name = field.name
            self._field_names.append(name)
            if config.camelize_json_keys:
                json_name = camelize(name, False)
                self._camelized_field_names.append(json_name)
            else:
                json_name = name
            types = cast(Types, self._get_types(field, config))
            types.fdef._cdef = self
            if isinstance(field.default, Types):
                default = None
            elif field.default == field.default_factory:
                default = None
            else:
                default = field.default
            jfield = JField(
                name=name,
                json_name=json_name,
                default=default,
                types=types,
                fdef=types.fdef,
                validator=types.validator)
            self._list_fields.append(jfield)
            self._dict_fields[name] = jfield
            if types.fdef.primary:
                self._primary_field = jfield
            if types.fdef.usage == 'created_at':
                self._created_at_field = jfield
            elif types.fdef.usage == 'updated_at':
                self._updated_at_field = jfield
            elif types.fdef.usage == 'deleted_at':
                self._deleted_at_field = jfield
            if types.fdef.field_storage == FieldStorage.LOCAL_KEY:
                key_transformer = config.key_transformer
                self._reference_names.append(key_transformer(jfield))
                if config.camelize_json_keys:
                    self._camelized_reference_names.append(
                        camelize(key_transformer(jfield), False))
            if types.fdef.delete_rule == DeleteRule.DENY:
                self._deny_fields.append(jfield)
            elif types.fdef.delete_rule == DeleteRule.NULLIFY:
                self._nullify_fields.append(jfield)
            elif types.fdef.delete_rule == DeleteRule.CASCADE:
                self._cascade_fields.append(jfield)
            if types.fdef.requires_operator_assign:
                self._assign_operator_fields.append(jfield)
        self._tuple_fields: tuple[JField] = tuple(self._list_fields)
        self._available_names: set[str] = set(self._field_names
                                              + self._camelized_field_names
                                              + self._reference_names
                                              + self._camelized_reference_names)
        self._update_names: set[str] = set(self._field_names
                                           + self._reference_names)

    def _get_types(self: Cdef,
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
            return rtypes(field.type, config)

    def _def_class_match(self: Cdef,
                         fdef: Fdef,
                         class_: type) -> bool:
        if fdef.field_type == FieldType.LIST:
            item_types = rtypes(fdef.raw_item_types, self.config)
            return self._def_class_match(item_types.fdef, class_)
        elif fdef.field_type == FieldType.INSTANCE:
            types = rtypes(fdef.raw_inst_types, self.config)
            return types.fdef.raw_inst_types == class_
        return False

    @property
    def cls(self: Cdef) -> type:
        """The JSON class on which this class definition is defined.
        """
        return self._cls

    @property
    def name(self: Cdef) -> str:
        """The name of the JSON class on which this class definition is
        defined.
        """
        return self._name

    @property
    def config(self: Cdef) -> Config:
        """The configuration object of the JSON class on which this class
        definition is defined.
        """
        return self._config

    def field_named(self: Cdef, name: str) -> JField:
        """
        Get the field which is named `name`.

        Args:
            name (str): The name of the field to return.

        Returns:
            JField: The field named `name`.

        Raises:
            ValueError: If can't find a field with name `name`.
        """
        if not self._dict_fields.get(name):
            raise ValueError(f'no field named {name} in class definition')
        return self._dict_fields[name]

    @property
    def fields(self: Cdef) -> tuple[JField]:
        """Get the fields of this class definition as a tuple. This is useful
        for looping and iterating.
        """
        return self._tuple_fields

    @property
    def created_at_field(self: Cdef) -> Optional[JField]:
        """
        The class definition's field which represents the created at field.

        This is used by the framework to locate the correct field to find the
        record's created at timestamp.
        """
        return self._created_at_field

    @property
    def updated_at_field(self: Cdef) -> Optional[JField]:
        """The class definition's field which represents the updated at field.

        This is used by the framework to locate the correct field to find the
        record's updated at timestamp.
        """
        return self._updated_at_field

    @property
    def deleted_at_field(self: Cdef) -> Optional[JField]:
        """The class definition's field which represents the deleted at field.

        This is used by the framework to locate the correct field to find the
        record's deleted at timestamp.
        """
        return self._deleted_at_field

    @property
    def deny_fields(self: Cdef) -> list[JField]:
        """Reference fields with deny delete rule.
        """
        return self._deny_fields

    @property
    def nullify_fields(self: Cdef) -> list[JField]:
        """Reference fields with nullify delete rule.
        """
        return self._nullify_fields

    @property
    def cascade_fields(self: Cdef) -> list[JField]:
        """Reference fields with cascade delete rule.
        """
        return self._cascade_fields

    @property
    def primary_field(self: Cdef) -> Optional[JField]:
        """The class definition's primary field. This can be None if it's not
        defined by user.
        """
        return self._primary_field

    @property
    def assign_operator_fields(self: Cdef) -> list[JField]:
        """The class definition's fields which require operator assigning on
        object creation.
        """
        return self._assign_operator_fields

    def foreign_field_for(self: Cdef,
                          name: str) -> Optional[tuple[Cdef, str]]:
        """Get the linked foreign field for local field named `name`.

        Args:
            name (str): The name of the local field.

        Returns:
            Optional[tuple[Cdef, str]]: A tuple which is a \
            combination of foreign class definition and foreign field name or \
            None if not found.

        Raises:
            LinkedFieldUnmatchException: A foreign field which is linked by \
            the field definition is found, however the properties don't match.
        """
        if name in self._foreign_fields:
            field_tuple = self._foreign_fields[name]
            if field_tuple is None:
                return None
            return field_tuple
        local_field = self.field_named(name)
        fdef = local_field.fdef
        if fdef.field_storage not in \
                [FieldStorage.LOCAL_KEY, FieldStorage.FOREIGN_KEY]:
            raise ValueError(f"field named '{name}' is not a linked field")
        if fdef.field_type == FieldType.INSTANCE:
            foreign_types = rtypes(fdef.raw_inst_types, self.config)
        elif fdef.field_type == FieldType.LIST:
            raw_inst_types = rtypes(fdef.raw_item_types, self.config)
            foreign_types = rtypes(raw_inst_types, self.config)
        foreign_class = cast(type, foreign_types.fdef.raw_inst_types)
        foreign_class = rtypes(foreign_class, self.config)
        foreign_class = foreign_class.fdef.raw_inst_types
        foreign_cdef = self.config.class_graph.fetch(foreign_class)
        accepted: list[tuple[FieldStorage, bool]] = []
        if fdef.field_storage == FieldStorage.LOCAL_KEY:
            foreign_storage = FieldStorage.FOREIGN_KEY
            use_join_table = False
            accepted.append((foreign_storage, use_join_table))
        elif fdef.field_storage == FieldStorage.FOREIGN_KEY:
            foreign_storage = FieldStorage.LOCAL_KEY
            use_join_table = False
            accepted.append((foreign_storage, use_join_table))
            if fdef.field_type == FieldType.LIST:
                foreign_storage = FieldStorage.FOREIGN_KEY
                use_join_table = True
                accepted.append((foreign_storage, use_join_table))
            elif fdef.field_type == FieldType.INSTANCE:
                pass
        for field in foreign_cdef.fields:
            for (storage, use_join) in accepted:
                if storage == FieldStorage.LOCAL_KEY:
                    if fdef.foreign_key == field.name:
                        local_matches = self._def_class_match(
                            local_field.fdef, foreign_class)
                        foreign_matches = self._def_class_match(
                            field.fdef, self.cls)
                        if local_matches and foreign_matches:
                            foreign_tuple = (foreign_cdef, field.name)
                            self._foreign_fields[name] = foreign_tuple
                            local_tuple = (self, name)
                            foreign_cdef._foreign_fields[field.name] = \
                                local_tuple
                            return self._foreign_fields[name]
                        else:
                            raise LinkedFieldUnmatchException(
                                self.cls.__name__, local_field.name,
                                foreign_class.__name__, field.name)
                elif storage == FieldStorage.FOREIGN_KEY:
                    if local_field.name == field.fdef.foreign_key:
                        if use_join == field.fdef.use_join_table:
                            local_matches = self._def_class_match(
                                local_field.fdef, foreign_class)
                            foreign_matches = self._def_class_match(
                                field.fdef, self.cls)
                            if local_matches and foreign_matches:
                                foreign_tuple = \
                                    (foreign_cdef, field.name)
                                self._foreign_fields[name] = foreign_tuple
                                local_tuple = (self, name)
                                foreign_cdef._foreign_fields[field.name]\
                                    = local_tuple
                                return self._foreign_fields[name]
                            else:
                                raise LinkedFieldUnmatchException(
                                    self.cls.__name__, local_field.name,
                                    foreign_class.__name__, field.name)
                        else:
                            raise LinkedFieldUnmatchException(
                                self.cls.__name__, local_field.name,
                                foreign_class.__name__, field.name)
        self._foreign_fields[name] = None
        return None
