from __future__ import annotations
from unittest import TestCase
from jsonclasses import jsonclass, ORMObject, types


class TestOnSaveVailidator(TestCase):

    def test_orm_objects_if_new_triggers_on_save(self):

        val = {'val': 0}

        def callback(value):
            val['val'] = val['val'] + 1

        @jsonclass(class_graph='test_onsave_0')
        class ClassOne(ORMObject):
            a: str = types.str.required
            b: int = types.int.onsave(callback).required
        item = ClassOne(a='a', b=1)
        item.a = 'b'
        item._setonsave()
        self.assertEqual(val, {'val': 1})

    def test_orm_objects_if_modified_trigger_onsave(self):
        val = {'val': 0}

        def callback(value):
            val['val'] = val['val'] + 1

        @jsonclass(class_graph='test_onsave_1')
        class ClassOne(ORMObject):
            a: str = types.str.required
            b: int = types.int.onsave(callback).required
        item = ClassOne(a='a', b=1)
        setattr(item, '_is_new', False)
        item.a = 'b'
        item._setonsave()
        self.assertEqual(val, {'val': 1})

    def test_orm_objects_if_modified_trigger_onsave_0_args(self):
        val = {'val': 0}

        def callback():
            val['val'] = val['val'] + 1

        @jsonclass(class_graph='test_onsave_2')
        class ClassOne(ORMObject):
            a: str = types.str.required
            b: int = types.int.onsave(callback).required
        item = ClassOne(a='a', b=1)
        setattr(item, '_is_new', False)
        item.a = 'b'
        item._setonsave()
        self.assertEqual(val, {'val': 1})

    def test_orm_objects_onsave_triggers_for_modified_linked_objects(self):
        u = {'u': 0}
        b1 = {'b1': 0}

        def ucallback():
            u['u'] += 1

        def b1callback():
            b1['b1'] += 1

        @jsonclass(class_graph='test_onsave_3')
        class User(ORMObject):
            id: int = types.int.primary.required
            name: str = types.str.required
            value: int = types.int.onsave(ucallback).required
            books: list[Book] = types.nonnull.listof('Book').linkedby('user').required

        @jsonclass(class_graph='test_onsave_3')
        class Book(ORMObject):
            id: int = types.int.primary.required
            name: str = types.str.required
            value: int = types.int.onsave(b1callback).required
            user: User = types.linkto.instanceof(User).required

        book1 = Book(id=1, name='B1', value=1)
        book2 = Book(id=2, name='B2', value=1)
        setattr(book1, '_is_new', False)
        setattr(book2, '_is_new', False)
        user = User(id=1, name='U', value=1)
        setattr(user, '_is_new', False)
        user.books.append(book1)
        user.books.append(book2)
        user._setonsave()

        self.assertEqual(u, {'u': 1})
        self.assertEqual(b1, {'b1': 2})
