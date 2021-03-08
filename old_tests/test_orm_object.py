from __future__ import annotations
from typing import Optional
from unittest import TestCase
from jsonclasses import jsonclass, ORMObject, types
from jsonclasses.exceptions import ValidationException, JSONClassResetNotEnabledError


class TestORMObject(TestCase):

    def test_existing_orm_object_only_validate_modified_fields(self):
        @jsonclass(class_graph='test_orm_6')
        class Product(ORMObject):
            name: str
            stock: int
        product = Product(name='p', stock=1)
        setattr(product, '_is_new', False)
        product.stock = 5
        product.name = None
        setattr(product, '_modified_fields', {'stock'})
        product.validate()

    def test_new_orm_object_validate_all_fields(self):
        @jsonclass(class_graph='test_orm_7')
        class Product(ORMObject):
            name: str
            stock: int
        product = Product(name='p', stock=1)
        product.stock = None
        product.name = None
        try:
            product.validate()
        except ValidationException as e:
            self.assertEqual(e.keypath_messages['name'], "Value at 'name' should not be None.")
            self.assertEqual(e.keypath_messages['stock'], "Value at 'stock' should not be None.")

    def test_orm_object_reference_fields_on_root_are_validated_anyway(self):

        @jsonclass(class_graph='test_orm_8')
        class User(ORMObject):
            id: int = types.int.primary
            name: str
            product: Product = types.instanceof('Product').linkedby('user')

        @jsonclass(class_graph='test_orm_8')
        class Product(ORMObject):
            id: int = types.int.primary
            name: str
            stock: int
            user: User = types.linkto.instanceof('User').required

        product = Product(**{
            'id': 1,
            'name': '2',
            'stock': 5,
            'user': {
                'id': 1,
                'name': 'u'
            }
        })
        setattr(product, '_is_new', False)
        product.user.name = None
        self.assertEqual(product.is_modified, False)
        self.assertEqual(product.modified_fields, set())
        self.assertRaisesRegex(ValidationException, "Value at 'user\\.name' should not be None\\.", product.validate)

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
