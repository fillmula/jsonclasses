"""
This module defines `CDef`. Each JSON class has its own class
definition. The class definition object contains detailed information about how
user defines a JSON class. This is used by the framework to lookup class fields
and class field settings.
"""
from __future__ import annotations
from jsonclasses.jobject import JObject
from typing import Optional, Any, final, cast, TYPE_CHECKING
from dataclasses import fields as dataclass_fields
from .jfield import JField
from .fdef import FStore, DeleteRule, FType
from .rtypes import rtypes, rnamedtypes
if TYPE_CHECKING:
    from .jconf import JConf


@final
class CDef:
    """Class definition represents the class definition of JSON classes. Each
    JSON class has its own class definition. The class definition object
    contains detailed information about how user defines a JSON class. This is
    used by the framework to lookup class fields and class field settings.
    """

    def __init__(self: CDef, cls: type[JObject], jconf: JConf) -> None:
        """
        Initialize a new class definition.

        Args:
            cls (type): The JSON class for which the class definition is \
                created.
            jconf (JConf): The configuration object for the targeted class.
        """
        from .types import Types
        self._ref_names_resolved = False
        self._ref_types_resolved = False
        self._cls = cls
        jconf._cls = cls
        self._name: str = cls.__name__
        self._jconf: JConf = jconf
        self._list_fields: list[JField] = []
        self._dict_fields: dict[str, JField] = {}
        self._primary_field: Optional[JField] = None
        self._calc_fields: list[JField] = []
        self._setter_fields: list[JField] = []
        self._deny_fields: list[JField] = []
        self._nullify_fields: list[JField] = []
        self._cascade_fields: list[JField] = []
        self._field_names: list[str] = []
        self._camelized_field_names: list[str] = []
        self._reference_names: list[str] = []
        self._camelized_reference_names: list[str] = []
        self._list_reference_names: list[str] = []
        self._camelized_list_reference_names: list[str] = []
        self._virtual_reference_names: list[str] = []
        self._camelized_virtual_reference_names: list[str] = []
        self._virtual_reference_fields: dict[str, JField] = {}
        self._unique_fields: list[JField] = []
        self._assign_operator_fields: list[JField] = []
        self._auth_identity_fields: list[JField] = []
        self._auth_by_fields: list[JField] = []
        self._rfmap: dict[str, JField] = {}
        for field in dataclass_fields(cls):
            name = field.name
            self._field_names.append(name)
            if isinstance(field.default, Types):
                types = field.default
                default = None
            elif field.default == cast(Any, field).default_factory:
                types = rtypes(field.type)
                default = None
            else:
                types = rtypes(field.type)
                default = field.default
            types.fdef._cdef = self
            jfield = JField(cdef=self, name=name, default=default, types=types)
            self._camelized_field_names.append(jfield.json_name)
            self._list_fields.append(jfield)
            self._dict_fields[name] = jfield
            if types.fdef._primary:
                self._primary_field = jfield
            if types.fdef._fstore == FStore.CALCULATED:
                self._calc_fields.append(jfield)
            if types.fdef._setter is not None:
                self._setter_fields.append(jfield)
            if types.fdef._delete_rule == DeleteRule.DENY:
                self._deny_fields.append(jfield)
            elif types.fdef._delete_rule == DeleteRule.NULLIFY:
                self._nullify_fields.append(jfield)
            elif types.fdef._delete_rule == DeleteRule.CASCADE:
                self._cascade_fields.append(jfield)
            if types.fdef._unique:
                self._unique_fields.append(jfield)
            if types.fdef._requires_operator_assign:
                self._assign_operator_fields.append(jfield)
            if types.fdef._auth_identity:
                self._auth_identity_fields.append(jfield)
            if types.fdef._auth_by:
                self._auth_by_fields.append(jfield)
        self._tuple_fields: tuple[JField, ...] = tuple(self._list_fields)

    @property
    def cls(self: CDef) -> type:
        """The JSON class on which this class definition is defined.
        """
        return self._cls

    @property
    def name(self: CDef) -> str:
        """The name of the JSON class on which this class definition is
        defined.
        """
        return self._name

    @property
    def jconf(self: CDef) -> JConf:
        """The configuration object of the JSON class on which this class
        definition is defined.
        """
        return self._jconf

    def field_named(self: CDef, name: str) -> JField:
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
    def fields(self: CDef) -> tuple[JField, ...]:
        """Get the fields of this class definition as a tuple. This is useful
        for looping and iterating.
        """
        return self._tuple_fields

    @property
    def calc_fields(self: CDef) -> list[JField]:
        """Calculated fields of this class definition.
        """
        return self._calc_fields

    @property
    def calc_field_names(self: CDef) -> list[str]:
        """Names of calculated fields.
        """
        if hasattr(self, '_calc_field_names'):
            return self._calc_field_names
        self._calc_field_names = list(map(lambda f: f.name, self._calc_fields))
        return self._calc_field_names

    @property
    def setter_fields(self: CDef) -> list[JField]:
        """Calculated fields with setter of this class definition.
        """
        return self._setter_fields

    @property
    def setter_field_names(self: CDef) -> list[str]:
        """Names of calculated fields with setter.
        """
        if hasattr(self, '_setter_field_names'):
            return self._setter_field_names
        self._setter_field_names = [f.name for f in self._setter_fields]
        return self._setter_field_names

    @property
    def deny_fields(self: CDef) -> list[JField]:
        """Reference fields with deny delete rule.
        """
        return self._deny_fields

    @property
    def nullify_fields(self: CDef) -> list[JField]:
        """Reference fields with nullify delete rule.
        """
        return self._nullify_fields

    @property
    def cascade_fields(self: CDef) -> list[JField]:
        """Reference fields with cascade delete rule.
        """
        return self._cascade_fields

    @property
    def primary_field(self: CDef) -> Optional[JField]:
        """The class definition's primary field. This can be None if it's not
        defined by user.
        """
        return self._primary_field

    @property
    def unique_fields(self: CDef) -> list[JField]:
        """The unique fields of this class definition.
        """
        return self._unique_fields

    @property
    def assign_operator_fields(self: CDef) -> list[JField]:
        """The class definition's fields which require operator assigning on
        object creation.
        """
        return self._assign_operator_fields

    @property
    def auth_identity_fields(self: CDef) -> list[JField]:
        """Auth identity fields.
        """
        return self._auth_identity_fields

    @property
    def auth_by_fields(self: CDef) -> list[JField]:
        """Auth by fields.
        """
        return self._auth_by_fields

    @property
    def available_names(self: CDef) -> set[str]:
        self._resolve_ref_names_if_needed()
        return self._available_names

    @property
    def update_names(self: CDef) -> set[str]:
        self._resolve_ref_names_if_needed()
        return self._update_names

    @property
    def reference_names(self: CDef) -> set[str]:
        self._resolve_ref_names_if_needed()
        return set(self._reference_names)

    @property
    def camelized_reference_names(self: CDef) -> set[str]:
        self._resolve_ref_names_if_needed()
        return set(self._camelized_reference_names)

    @property
    def list_reference_names(self: CDef) -> set[str]:
        self._resolve_ref_names_if_needed()
        return set(self._list_reference_names)

    @property
    def camelized_list_reference_names(self: CDef) -> set[str]:
        self._resolve_ref_names_if_needed()
        return set(self._camelized_list_reference_names)

    @property
    def virtual_reference_names(self: CDef) -> set[str]:
        self._resolve_ref_names_if_needed()
        return set(self._virtual_reference_names)

    @property
    def camelized_virtual_reference_names(self: CDef) -> set[str]:
        self._resolve_ref_names_if_needed()
        return set(self._camelized_virtual_reference_names)

    @property
    def virtual_reference_fields(self: CDef) -> dict[str, JField]:
        self._resolve_ref_names_if_needed()
        return self._virtual_reference_fields

    def rname_to_jfield(self: CDef, ref_name: str) -> JField:
        self._resolve_ref_names_if_needed()
        return self._rfmap[ref_name]

    def rfield(
            self: CDef, fcls: type[JObject], fname: Optional[str],
            fkey: Optional[str]) -> Optional[JField]:
        for field in self._tuple_fields:
            if field.foreign_class is fcls:
                if fname is not None:
                    if field.name == fname:
                        return field
                elif fkey is not None:
                    if field.fdef.foreign_key == fkey:
                        return field
        else:
            return None

    def _resolve_ref_types_if_needed(self: CDef) -> None:
        if self._ref_types_resolved is False:
            self._resolve_types()
            self._ref_types_resolved = True

    def _resolve_ref_names_if_needed(self: CDef) -> None:
        if self._ref_names_resolved is False:
            self._resolve_ref_names()
            self._ref_names_resolved = True

    def _resolve_types(self: CDef) -> None:
        for jfield in self._tuple_fields:
            if jfield.types.fdef._unresolved:
                cgraph = self.jconf.cgraph
                jfield._types = rnamedtypes(jfield.types, cgraph, self.name)

    def _resolve_ref_names(self: CDef) -> None:
        for jfield in self._tuple_fields:
            if jfield.types.fdef._fstore == FStore.LOCAL_KEY:
                ref_name_strategy = self.jconf.ref_name_strategy
                if jfield.fdef.ftype == FType.INSTANCE:
                    self._reference_names.append(ref_name_strategy(jfield))
                    self._camelized_reference_names.append(
                        self.jconf.output_key_strategy(ref_name_strategy(jfield)))
                    self._rfmap[ref_name_strategy(jfield)] = jfield
                elif jfield.fdef.ftype == FType.LIST:
                    self._list_reference_names.append(ref_name_strategy(jfield))
                    self._camelized_list_reference_names.append(
                        self.jconf.output_key_strategy(ref_name_strategy(jfield)))
                    self._rfmap[ref_name_strategy(jfield)] = jfield
            elif jfield.types.fdef._fstore == FStore.FOREIGN_KEY:
                if jfield.types.fdef._use_join_table:
                    rkes = self.jconf.ref_name_strategy
                    jkes = self.jconf.output_key_strategy
                    rk = rkes(jfield)
                    self._virtual_reference_names.append(rk)
                    self._camelized_virtual_reference_names.append(jkes(rk))
                    self._virtual_reference_fields[rk] = jfield
                    self._rfmap[rk] = jfield
        self._available_names: set[str] = set(self._field_names
                                              + self._camelized_field_names
                                              + self._reference_names
                                              + self._camelized_reference_names
                                              + self._list_reference_names
                                              + self._camelized_list_reference_names)
        self._update_names: set[str] = set(self._field_names
                                           + self._reference_names
                                           + self._list_reference_names)
