"""This module contains `JSONObject`, the main base class of JSON Classes.
"""
from __future__ import annotations
from typing import Any, Optional, ClassVar, Union, TypeVar
from dataclasses import dataclass, fields as dataclass_fields
from .config import Config
from .exceptions import ValidationException, AbstractJSONClassException
from .fields import (FieldType, Field, get_fields, other_field, field,
                     is_reference_field, updated_at_field)
from .validators.instanceof_validator import InstanceOfValidator
from .contexts import TransformingContext, ValidatingContext, ToJSONContext
from .owned_dict import OwnedDict
from .owned_list import OwnedList
from .object_graph import ObjectGraph
from .keypath import concat_keypath


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

    @classmethod
    def fields(cls: type[T]) -> list[Field]:
        """Returns all JSON fields of this JSON class.
        """
        return get_fields(cls)

    @classmethod
    def primary_field(cls: type[T]) -> Optional[Field]:
        k = '_primary_fields'
        if hasattr(cls, k) and getattr(cls, k) is not None:
            return getattr(cls, k)
        pf = next((f for f in cls.fields() if f.fdesc.primary is True), None)
        setattr(cls, k, pf)
        return pf

    def __init__(self: T, **kwargs: Any) -> None:
        """Initialize a new jsonclass object from keyed arguments or a dict.
        This method is suitable for accepting web and malformed inputs. Eager
        validation and transformation are applied during the initialization
        process.
        """
        if self.__class__.config.abstract:
            raise AbstractJSONClassException(self.__class__)
        for f in dataclass_fields(self):
            setattr(self, f.name, None)
        self.__set(fill_blanks=True, **kwargs)

    @property
    def _id(self: T) -> Optional[Union[str, int]]:
        primary_field = self.__class__.primary_field()
        if primary_field is None:
            return None
        return getattr(self, primary_field.field_name)

    def set(self: T, **kwargs: Any) -> T:
        """Set object values in a batch. This method is suitable for web and
        fraud inputs. This method takes accessor marks into consideration,
        means readonly and internal field values will be just ignored.
        Writeonce fields are accepted only if the current value is None. This
        method triggers eager validation and transform. This method returns
        self, thus you can chain calling with other instance methods.
        """
        self._detached_test()
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
            object_graph=self._graph)
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
        self._detached_test()
        unallowed_keys = set(kwargs.keys()) - set(self.__fdict__.keys())
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
        self._detached_test()
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
        self._detached_test()
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
            object_graph=ObjectGraph())
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

    @property
    def is_detached(self: T) -> bool:
        """This property marks during object graph merging, this object doesn't
        represent the newest object status and thus deteched from the graph and
        become orphan and cannot be used.
        """
        if not hasattr(self, '_is_detached'):
            self._is_detached = False
        return self._is_detached

    def _detached_test(self: T) -> None:
        if self.is_detached:
            raise ValueError(f'JSON object {self} is detached')
        if (hasattr(self, '_is_deleted')
           and getattr(self, '_is_deleted') is True):
            raise ValueError(f'JSON object {self} is deleted')

    @property
    def _graph(self: T) -> ObjectGraph:
        """The JSON Object's object graph.
        """
        if not hasattr(self, '_graph_'):
            setattr(self, '_graph_', ObjectGraph())
        return self._graph_

    @_graph.setter
    def _graph(self: T, val: ObjectGraph) -> None:
        self._graph_ = val

    def _compare(self: T, old: T, new: T) -> T:
        from .orm_object import ORMObject
        if not isinstance(old, ORMObject):  # old and new have same class
            raise ValueError((f'graph merging conflict on {old} and {new}, '
                              'please use ORMObject'))
        if old.is_detached:
            return new
        if new.is_detached:
            return old
        ua_field = updated_at_field(old)  # old and new have same fields
        if ua_field is None:
            raise ValueError((f'graph merging conflict on {old} and {new}, '
                              'please record updated at timestamp'))
        ua_old = getattr(old, ua_field.field_name)
        ua_new = getattr(new, ua_field.field_name)
        if ua_old == ua_new:
            if not new.is_modified and not old.is_modified:
                return new  # return any if both not modified
            if new.is_modified and not old.is_modified:
                return new
            if old.is_modified and not new.is_modified:
                return old
            raise ValueError((f'graph merging conflict on {old} and {new},'
                              ' both are modified'))
        if ua_old is None:
            return new
        if ua_new is None:
            return old
        return new if ua_new > ua_old else old

    def _replace_refs(self: T, old: T, new: T):
        old_fields = old.__class__.fields()
        for old_field in old_fields:
            if not is_reference_field(old_field):
                continue
            val = getattr(old, old_field.field_name)
            items: list[JSONObject] = []
            if isinstance(val, JSONObject):
                items = [val]
            if isinstance(val, list):
                items = val
            for item in items:
                oth_field = other_field(old, item, old_field)
                other_value = getattr(item, oth_field.field_name)
                if other_value is old:
                    setattr(old, '_is_detached', True)
                    setattr(item, oth_field.field_name, new)
                if isinstance(other_value, list):
                    try:
                        i = other_value.index(old)
                        setattr(old, '_is_detached', True)
                        other_value[i] = new
                    except ValueError:
                        continue

    def _merge_graph(self: T, obj: T) -> None:
        graph1 = self._graph
        graph2 = obj._graph
        if graph1 is graph2:
            return
        for o in graph2:
            if o._graph is not graph1:
                if graph1.has(o):
                    o_in_1 = graph1.get(o)
                    if o_in_1 is o:
                        o_in_1._graph = graph1
                        continue
                    o_to_keep = self._compare(o_in_1, o)
                    if o_in_1 is o_to_keep:
                        o_in_2 = o
                        self._replace_refs(o_in_2, o_in_1)
                        setattr(o_in_2, '_is_modified', False)
                        setattr(o_in_2, '_is_detached', True)
                    else:
                        graph1.put(o_to_keep)
                        o_to_keep._graph = graph1
                        self._replace_refs(o_in_1, o_to_keep)
                        setattr(o_in_1, '_is_modified', False)
                        setattr(o_in_1, '_is_detached', True)
                else:
                    graph1.put(o)
                    o._graph = graph1

    def _link_graph(self: T, obj: T) -> None:
        self._merge_graph(obj)

    @property
    def __fdict__(self: T) -> dict[str, Any]:
        """Purified dict contains __dict__ items only for fields.
        """
        retval = {}
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                retval[k] = v
        return retval

    def __setattr_direct__(self: T, name: str, value: Any) -> None:
        super().__setattr__(name, value)

    def _owned_list(self: T, lst: list, kpath: str) -> OwnedList:
        new_lst = []
        for i, v in enumerate(lst):
            if isinstance(v, list):
                new_lst.append(self._owned_list(v, concat_keypath(kpath, i)))
            elif isinstance(v, dict):
                new_lst.append(self._owned_dict(v, concat_keypath(kpath, i)))
            else:
                new_lst.append(v)
        owned_list = OwnedList[Any](new_lst)
        owned_list.keypath = kpath
        owned_list.owner = self
        return owned_list

    def _owned_dict(self: T, dct: dict, kpath: str) -> OwnedDict:
        new_dct = {}
        for k, v in dct.items():
            if isinstance(v, list):
                new_dct[k] = self._owned_list(v, concat_keypath(kpath, k))
            elif isinstance(v, dict):
                new_dct[k] = self._owned_dict(v, concat_keypath(kpath, k))
            else:
                new_dct[k] = v
        owned_dict = OwnedDict[Any](new_dct)
        owned_dict.keypath = kpath
        owned_dict.owner = self
        return owned_dict

    def __setattr__(self: T, name: str, value: Any) -> None:
        if name.startswith('_'):  # private fields
            super().__setattr__(name, value)
            return
        # self._detached_test()
        tfield = field(self, name)
        if tfield is None:  # not json class field
            super().__setattr__(name, value)
            return
        if isinstance(value, list):  # json class mutable list collection
            value = self._owned_list(value, name)
        if isinstance(value, dict):  # json class mutable dict collection
            value = self._owned_dict(value, name)
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

    def __odict_will_change__(self, odict: OwnedDict) -> None:
        pass

    def __odict_add__(self, odict: OwnedDict, key: str, val: Any) -> None:
        if isinstance(val, dict):
            odict[key] = self._owned_dict(val,
                                          concat_keypath(odict.keypath, key))
        if isinstance(val, list):
            odict[key] = self._owned_list(val,
                                          concat_keypath(odict.keypath, key))

    def __odict_del__(self, odict: OwnedDict, val: Any) -> None:
        pass

    def __olist_will_change__(self, olist: OwnedList) -> None:
        pass

    def __olist_add__(self, olist: OwnedList, idx: int, val: Any) -> None:
        tfield = field(self, olist.keypath)
        if tfield is not None and is_reference_field(tfield):
            self.__link_field__(tfield, [val])
            return
        if isinstance(val, dict):
            olist[idx] = self._owned_dict(val,
                                          concat_keypath(olist.keypath, idx))
        if isinstance(val, list):
            olist[idx] = self._owned_list(val,
                                          concat_keypath(olist.keypath, idx))

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
            self._link_graph(item)


T = TypeVar('T', bound=JSONObject)
