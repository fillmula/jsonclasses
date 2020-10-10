"""This module contains `JSONObject`, the main base class of JSON Classes.
"""
from __future__ import annotations
from typing import Any, Optional, ClassVar, TypeVar
from dataclasses import dataclass, fields as dataclass_fields
from .config import Config
from .exceptions import ValidationException
from .fields import FieldType, Field, other_field, field, is_reference_field
from .validators.instanceof_validator import InstanceOfValidator
from .contexts import TransformingContext, ValidatingContext, ToJSONContext
from .lookup_map import LookupMap
from .owned_dict import OwnedDict
from .owned_list import OwnedList


@dataclass(init=False)
class JSONObject:
    """JSONObject is the base class of JSON Classes objects. It provides
    crutial instance methods e.g. __init__, set, update, validate and tojson.

    To declare a new JSON Class, use the following syntax:

      from jsonclasses import jsonclass, JSONObject, types

      @jsonclass
      class MyObject(JSONObject):
        my_field_one: str = types.str.required
        my_field_two: int = types.int.range(0, 10).required
    """

    config: ClassVar[Config]

    def __init__(self: T, **kwargs: Any) -> None:
        """Initialize a new jsonclass object from keyed arguments or a dict.
        This method is suitable for accepting web and malformed inputs. Eager
        validation and transformation are applied during the initialization
        process.
        """
        for f in dataclass_fields(self):
            setattr(self, f.name, None)
        self.__set(fill_blanks=True, **kwargs)

    def set(self: T, **kwargs: Any) -> T:
        """Set object values in a batch. This method is suitable for web and
        fraud inputs. This method takes accessor marks into consideration,
        means readonly and internal field values will be just ignored.
        Writeonce fields are accepted only if the current value is None. This
        method triggers eager validation and transform. This method returns
        self, thus you can chain calling with other instance methods.
        """
        self.__set(fill_blanks=False, **kwargs)
        return self

    def __set(self: T, fill_blanks: bool = False, **kwargs: Any) -> None:
        """Set values of a JSON Class object internally."""
        validator = InstanceOfValidator(self.__class__)
        config = self.__class__.config
        context = TransformingContext(
            value=kwargs,
            keypath_root='',
            root=self,
            config_root=config,
            keypath_owner='',
            owner=self,
            config_owner=config,
            keypath_parent='',
            parent=self,
            fdesc=None,
            all_fields=True,
            dest=self,
            fill_dest_blanks=fill_blanks,
            lookup_map=LookupMap())
        validator.transform(context)

    def update(self: T, **kwargs: Any) -> T:
        """Update object values in a batch. This method is suitable for
        internal inputs. This method ignores accessor marks, thus you can
        update readonly and internal values through this method. Writeonce
        doesn't have effect on this method. You can change writeonce fields'
        value freely in this method. This method does not trigger eager
        validation and transform. You should pass valid and final form values
        through this method. This method returns self, thus you can chain
        calling with other instance methods.
        """
        unallowed_keys = set(kwargs.keys()) - set(self.__dict__.keys())
        unallowed_keys_length = len(unallowed_keys)
        if unallowed_keys_length > 0:
            keys_list = ', '.join(list(unallowed_keys))
            raise ValueError(f'`{keys_list}` not allowed in '
                             f'{self.__class__.__name__}.')
        for key, item in kwargs.items():
            setattr(self, key, item)
        return self

    def tojson(self: T, ignore_writeonly: bool = False) -> dict[str, Any]:
        """Serialize this JSON Class object to JSON dict.

        Args:
          ignore_writeonly (Optional[bool]): Whether ignore writeonly marks on
          fields. Be careful when setting it to True.

        Returns:
          dict: A dict represents this object's JSON object.
        """
        validator = InstanceOfValidator(self.__class__)
        config = self.__class__.config
        context = ToJSONContext(value=self,
                                config=config,
                                ignore_writeonly=ignore_writeonly)
        return validator.tojson(context)

    def validate(self: T, all_fields: Optional[bool] = None) -> T:
        """Validate the jsonclass object's validity. Raises ValidationException
        on validation failed.

        Args:
          all_fields (bool): Whether continue validation to fetch more error
          messages after the first error is found. This is useful when you are
          building a frontend form and want to display detailed messages.

        Returns:
          None: upon successful validation, returns nothing.
        """
        config = self.__class__.config
        context = ValidatingContext(
            value=self,
            keypath_root='',
            root=self,
            config_root=config,
            keypath_owner='',
            owner=self,
            config_owner=config,
            keypath_parent='',
            parent=self,
            fdesc=None,
            all_fields=all_fields,
            lookup_map=LookupMap())
        InstanceOfValidator(self.__class__).validate(context)
        return self

    def is_valid(self: T) -> bool:
        """Test whether the jsonclass object is valid or not. This method
        triggers object validation.

        Returns:
          bool: the validity of the object.
        """
        try:
            self.validate(all_fields=False)
        except ValidationException:
            return False
        return True

    def __setattr_direct__(self: T, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def __setattr__(self: T, name: str, value: Any) -> None:
        if name.startswith('_'):  # private fields
            super().__setattr__(name, value)
            return
        tfield = field(self, name)
        if tfield is None:  # not json class field
            super().__setattr__(name, value)
            return
        if isinstance(value, list):  # json class mutable list collection
            value = OwnedList[Any](value)
            value.owner = self
            value.keypath = name
        if isinstance(value, dict):  # json class mutable dict collection
            value = OwnedDict[str, Any](value)
            value.owner = self
            value.keypath = name
        if is_reference_field(tfield):  # json class ref field
            should_link = True
            if hasattr(self, name):
                old_value = getattr(self, name)
                should_link = old_value is not value
                if should_link:
                    self.__unlink_field__(tfield, old_value)
            super().__setattr__(name, value)
            if should_link:
                self.__link_field__(tfield, value)
            return
        super().__setattr__(name, value)  # json class normal field

    def __odict_add__(self, odict: OwnedDict, key: str, val: Any) -> None:
        pass

    def __odict_del__(self, odict: OwnedDict, val: Any) -> None:
        pass

    def __olist_add__(self, olist: OwnedList, idx: int, val: Any) -> None:
        tfield = field(self, olist.keypath)
        if tfield is None:
            return
        if not is_reference_field(tfield):
            return
        self.__link_field__(tfield, [val])

    def __olist_del__(self, olist: OwnedList, val: Any) -> None:
        tfield = field(self, olist.keypath)
        if tfield is None:
            return
        if not is_reference_field(tfield):
            return
        self.__unlink_field__(tfield, [val])

    def __olist_sor__(self, olist: OwnedList) -> None:
        pass

    def __unlink_field__(self, field: Field, value: Any) -> None:
        items: list[JSONObject] = []
        if field.fdesc.field_type == FieldType.INSTANCE:
            if not isinstance(value, JSONObject):
                return
            items = [value]
        if field.fdesc.field_type == FieldType.LIST:
            if not isinstance(value, list):
                return
            items = list(value)
        for item in items:
            ofield = other_field(self, item, field)
            if ofield is None:
                return
            if ofield.fdesc.field_type == FieldType.INSTANCE:
                if getattr(item, ofield.field_name) is self:
                    item.__setattr_direct__(ofield.field_name, None)
            elif ofield.fdesc.field_type == FieldType.LIST:
                that_list = getattr(item, ofield.field_name)
                if isinstance(that_list, list):
                    if self in that_list:
                        that_list.remove(self)

    def __link_field__(self, field: Field, value: Any) -> None:
        items: list[JSONObject] = []
        if field.fdesc.field_type == FieldType.INSTANCE:
            if not isinstance(value, JSONObject):
                return
            items = [value]
        if field.fdesc.field_type == FieldType.LIST:
            if not isinstance(value, list):
                return
            items = value
        for item in items:
            ofield = other_field(self, item, field)
            if ofield is None:
                return
            if ofield.fdesc.field_type == FieldType.INSTANCE:
                if getattr(item, ofield.field_name) != self:
                    setattr(item, ofield.field_name, self)
            elif ofield.fdesc.field_type == FieldType.LIST:
                if not isinstance(getattr(item, ofield.field_name), list):
                    setattr(item, ofield.field_name, [self])
                else:
                    if self not in getattr(item, ofield.field_name):
                        getattr(item, ofield.field_name).append(self)


T = TypeVar('T', bound=JSONObject)
