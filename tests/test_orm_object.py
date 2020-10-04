from __future__ import annotations
from typing import List
import unittest
from jsonclasses import jsonclass, ORMObject, types
from datetime import datetime


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

    def test_orm_object_has_modified_fields_and_defaults_to_empty_list(self):
        object = ORMObject()
        self.assertEqual(object.modified_fields, [])

    def test_orm_object_has_modified_fields_and_can_be_set(self):
        object = ORMObject()
        setattr(object, '_modified_fields', ['id'])
        self.assertEqual(object.modified_fields, ['id'])

    def test_orm_object_triggers_is_modified_on_field_change(self):
        @jsonclass(graph='test_orm_1')
        class Product(ORMObject):
            name: str
            stock: int
        product = Product(name='p', stock=1)
        self.assertEqual(product.is_modified, False)
        product.name = 'r'
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, ['name'])
        product.stock = 2
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, ['name', 'stock'])
        product.name = 'a'
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, ['name', 'stock'])

    def test_orm_object_triggers_is_modified_on_set_change(self):
        @jsonclass(graph='test_orm_2')
        class Product(ORMObject):
            name: str
            stock: int
        product = Product(name='p', stock=1)
        self.assertEqual(product.is_modified, False)
        product.set(name='h')
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, ['name'])
        product.set(stock=7)
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, ['name', 'stock'])
        product.set(name='c')
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, ['name', 'stock'])

    def test_orm_object_triggers_is_modified_on_update_change(self):
        @jsonclass(graph='test_orm_3')
        class Product(ORMObject):
            name: str
            stock: int
        product = Product(name='p', stock=1)
        self.assertEqual(product.is_modified, False)
        product.update(name='h')
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, ['name'])
        product.update(stock=7)
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, ['name', 'stock'])
        product.update(name='c')
        self.assertEqual(product.is_modified, True)
        self.assertEqual(product.modified_fields, ['name', 'stock'])


    # def test_persistable_json_object_has_created_at_on_initializing(self):
    #     o = ORMObject()
    #     self.assertTrue(type(o.created_at) is datetime)
    #     self.assertTrue(o.created_at < datetime.now())

    # def test_persistable_json_object_has_updated_at_on_initializing(self):
    #     o = ORMObject()
    #     self.assertTrue(type(o.updated_at) is datetime)
    #     self.assertTrue(o.updated_at < datetime.now())

    # def test_persistable_json_object_has_id_with_default_value_none(self):
    #     o = ORMObject()
    #     self.assertTrue(o.id is None)

    # def test_persistable_json_object_id_can_be_int(self):
    #     o = ORMObject()
    #     o.id = 5
    #     self.assertTrue(o.is_valid())

    # def test_persistable_json_object_id_can_be_str(self):
    #     o = ORMObject()
    #     o.id = "sbd"
    #     self.assertTrue(o.is_valid())

    # def test_persistable_json_object_id_can_be_none(self):
    #     o = ORMObject()
    #     o.id = None
    #     self.assertTrue(o.is_valid())

    # def test_persistable_json_object_has_timestamps_in_nested_instances(self):
    #     @jsonclass(graph='test_persistable_json_01')
    #     class TestAuthor(ORMObject):
    #         name: str
    #         posts: List[TestPost] = types.listof('TestPost').linkedby('author')

    #     @jsonclass(graph='test_persistable_json_01')
    #     class TestPost(ORMObject):
    #         title: str
    #         content: str
    #         author: TestAuthor = types.linkto.instanceof(TestAuthor)
    #     input = {
    #         'name': 'John Lesque',
    #         'posts': [
    #             {
    #                 'title': 'Post One',
    #                 'content': 'Great Article on Python.'
    #             },
    #             {
    #                 'title': 'Post Two',
    #                 'content': 'Great Article on JSON Classes.'
    #             }
    #         ]
    #     }
    #     author = TestAuthor(**input)
    #     self.assertIs(type(author.created_at), datetime)
    #     self.assertIs(type(author.updated_at), datetime)
    #     self.assertIs(type(author.posts[0].created_at), datetime)
    #     self.assertIs(type(author.posts[0].updated_at), datetime)
    #     self.assertIs(type(author.posts[1].created_at), datetime)
    #     self.assertIs(type(author.posts[1].updated_at), datetime)
