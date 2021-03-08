from __future__ import annotations
from typing import Optional
from unittest import TestCase
from jsonclasses import jsonclass, ORMObject
from jsonclasses.exceptions import JSONClassResetNotEnabledError


class TestORMObject(TestCase):

    def test_orm_object_records_previous_str_value(self):

        @jsonclass(class_graph='test_orm_9', reset_all_fields=True)
        class Data(ORMObject):
            str_field: Optional[str]
            int_field: Optional[int]
            list_field: Optional[list[str]]
            dict_field: Optional[dict[str, list[int]]]

        obj = Data(str_field='123', int_field=123)
        setattr(obj, '_is_new', False)
        obj.str_field = '234'
        self.assertEqual(obj.previous_values, {'str_field': '123'})

    def test_orm_object_records_previous_optional_int_value(self):

        @jsonclass(class_graph='test_orm_10', reset_all_fields=True)
        class Data(ORMObject):
            str_field: Optional[str]
            int_field: Optional[int]
            list_field: Optional[list[str]]
            dict_field: Optional[dict[str, list[int]]]

        obj = Data(str_field='123')
        setattr(obj, '_is_new', False)
        obj.str_field = '234'
        obj.int_field = 123
        self.assertEqual(obj.previous_values, {'str_field': '123', 'int_field': None})

    def test_orm_object_records_previous_list_value(self):

        @jsonclass(class_graph='test_orm_11', reset_all_fields=True)
        class Data(ORMObject):
            str_field: Optional[str]
            int_field: Optional[int]
            list_field: Optional[list[str]]
            dict_field: Optional[dict[str, list[int]]]

        obj = Data(list_field=[1, 2, 3])
        setattr(obj, '_is_new', False)
        obj.list_field.append(4)
        self.assertEqual(obj.previous_values, {'list_field': [1, 2, 3]})

    def test_orm_object_records_previous_dict_value(self):

        @jsonclass(class_graph='test_orm_12', reset_all_fields=True)
        class Data(ORMObject):
            str_field: Optional[str]
            int_field: Optional[int]
            list_field: Optional[list[str]]
            dict_field: Optional[dict[str, list[int]]]

        obj = Data(dict_field={'a': [1, 2, 3], 'b': [4, 5, 6]})
        setattr(obj, '_is_new', False)
        obj.dict_field['a'].append(4)
        self.assertEqual(obj.previous_values, {'dict_field': {'a': [1, 2, 3], 'b': [4, 5, 6]}})

    def test_orm_object_resets_previous_str_value(self):

        @jsonclass(class_graph='test_orm_13', reset_all_fields=True)
        class Data(ORMObject):
            str_field: Optional[str]
            int_field: Optional[int]
            list_field: Optional[list[str]]
            dict_field: Optional[dict[str, list[int]]]

        obj = Data(str_field='123', int_field=123)
        setattr(obj, '_is_new', False)
        obj.str_field = '234'
        obj.reset()
        self.assertEqual(obj, Data(str_field='123', int_field=123))

    def test_orm_object_resets_previous_optional_int_value(self):

        @jsonclass(class_graph='test_orm_14', reset_all_fields=True)
        class Data(ORMObject):
            str_field: Optional[str]
            int_field: Optional[int]
            list_field: Optional[list[str]]
            dict_field: Optional[dict[str, list[int]]]

        obj = Data(str_field='123')
        setattr(obj, '_is_new', False)
        obj.str_field = '234'
        obj.int_field = 123
        obj.reset()
        self.assertEqual(obj, Data(str_field='123'))

    def test_orm_object_resets_previous_list_value(self):

        @jsonclass(class_graph='test_orm_15', reset_all_fields=True)
        class Data(ORMObject):
            str_field: Optional[str]
            int_field: Optional[int]
            list_field: Optional[list[str]]
            dict_field: Optional[dict[str, list[int]]]

        obj = Data(list_field=[1, 2, 3])
        setattr(obj, '_is_new', False)
        obj.list_field.append(4)
        obj.reset()
        self.assertEqual(obj, Data(list_field=[1, 2, 3]))

    def test_orm_object_resets_previous_dict_value(self):

        @jsonclass(class_graph='test_orm_16', reset_all_fields=True)
        class Data(ORMObject):
            str_field: Optional[str]
            int_field: Optional[int]
            list_field: Optional[list[str]]
            dict_field: Optional[dict[str, list[int]]]

        obj = Data(dict_field={'a': [1, 2, 3], 'b': [4, 5, 6]})
        setattr(obj, '_is_new', False)
        obj.dict_field['a'].append(4)
        obj.reset()
        self.assertEqual(obj, Data(dict_field={'a': [1, 2, 3], 'b': [4, 5, 6]}))

    def test_orm_object_wont_record_previous_value_without_reset_all_fields(self):

        @jsonclass(class_graph='test_orm_17')
        class Data(ORMObject):
            str_field: Optional[str]
            int_field: Optional[int]
            list_field: Optional[list[str]]
            dict_field: Optional[dict[str, list[int]]]

        obj = Data(str_field='123')
        setattr(obj, '_is_new', False)
        obj.str_field = '234'
        self.assertEqual(obj.previous_values, {})

    def test_orm_object_wont_reset_previous_value_without_reset_all_fields(self):

        @jsonclass(class_graph='test_orm_18')
        class Data(ORMObject):
            str_field: Optional[str]
            int_field: Optional[int]
            list_field: Optional[list[str]]
            dict_field: Optional[dict[str, list[int]]]

        obj = Data(str_field='123')
        setattr(obj, '_is_new', False)
        obj.str_field = '234'

        self.assertRaises(JSONClassResetNotEnabledError, obj.reset)
