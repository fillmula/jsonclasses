from __future__ import annotations
from jsonclasses.exceptions import ValidationException
from typing import List
import unittest
from jsonclasses import jsonclass, ORMObject, types


class TestORMObject(unittest.TestCase):

    def test_orm_object_has_is_new_and_defaults_to_true(self):
        object = ORMObject()
        self.assertEqual(object.is_new, True)

    def test_orm_object_has_is_new_and_can_be_set_to_false(self):
        object = ORMObject()
        setattr(object, '_is_new', False)
        self.assertEqual(object.is_new, False)

    def test_orm_object_has_is_modified_and_defaults_to_false(self):
        object = ORMObject()
        self.assertEqual(object.is_modified, False)

    def test_orm_object_has_is_modified_and_can_be_set_to_true(self):
        object = ORMObject()
        setattr(object, '_is_modified', True)
        self.assertEqual(object.is_modified, True)

    def test_orm_object_has_modified_fields_and_defaults_to_empty_set(self):
        object = ORMObject()
        self.assertEqual(object.modified_fields, set())

    def test_orm_object_has_modified_fields_and_can_be_set(self):
        object = ORMObject()
        setattr(object, '_modified_fields', {'id'})
        self.assertEqual(object.modified_fields, {'id'})

    def test_orm_object_triggers_is_modified_on_field_change(self):
        @jsonclass(graph='test_orm_1')
        class Product(ORMObject):
            name: str
            stock: int
        product = Product(name='p', stock=1)
        setattr(product, '_is_new', False)
        self.assertEqual(product.is_modified, False)
        product.name = 'r'
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, {'name'})
        product.stock = 2
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, {'name', 'stock'})
        product.name = 'a'
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, {'name', 'stock'})

    def test_orm_object_triggers_is_modified_on_set_change(self):
        @jsonclass(graph='test_orm_2')
        class Product(ORMObject):
            name: str
            stock: int
        product = Product(name='p', stock=1)
        setattr(product, '_is_new', False)
        self.assertEqual(product.is_modified, False)
        product.set(name='h')
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, {'name'})
        product.set(stock=7)
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, {'name', 'stock'})
        product.set(name='c')
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, {'name', 'stock'})

    def test_orm_object_triggers_is_modified_on_update_change(self):
        @jsonclass(graph='test_orm_3')
        class Product(ORMObject):
            name: str
            stock: int
        product = Product(name='p', stock=1)
        setattr(product, '_is_new', False)
        self.assertEqual(product.is_modified, False)
        product.update(name='h')
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, {'name'})
        product.update(stock=7)
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, {'name', 'stock'})
        product.update(name='c')
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, {'name', 'stock'})

    def test_orm_object_triggers_is_modified_on_mark_list_update(self):
        @jsonclass(graph='test_orm_4')
        class Product(ORMObject):
            name: str
            variants: List[str]
        product = Product(name='p', variants=['xs', 's'])
        setattr(product, '_is_new', False)
        self.assertEqual(product.is_modified, False)
        product.variants.append('m')
        self.assertEqual(product.is_modified, False)
        product.mark_modified('variants')
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, {'variants'})

    def test_orm_object_doesnt_track_modified_for_new_objects(self):
        @jsonclass(graph='test_orm_5')
        class Product(ORMObject):
            name: str
            stock: int
        product = Product(name='p', stock=1)
        product.update(name='h')
        self.assertEqual(product.is_modified, False)
        self.assertEqual(product.modified_fields, set())
        product.set(name='q')
        self.assertEqual(product.is_modified, False)
        self.assertEqual(product.modified_fields, set())
        product.name = 'i'
        self.assertEqual(product.is_modified, False)
        self.assertEqual(product.modified_fields, set())

    def test_existing_orm_object_only_validate_modified_fields(self):
        @jsonclass(graph='test_orm_6')
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
        @jsonclass(graph='test_orm_7')
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

        @jsonclass(graph='test_orm_8')
        class User(ORMObject):
            id: int
            name: str
            product: Product = types.instanceof('Product').linkedby('user')

        @jsonclass(graph='test_orm_8')
        class Product(ORMObject):
            id: int
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
