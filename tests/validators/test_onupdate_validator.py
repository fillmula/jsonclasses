from __future__ import annotations
from unittest import TestCase
from jsonclasses import jsonclass, ORMObject, types


class TestOnUpdateVailidator(TestCase):

    def test_orm_objects_if_new_do_not_trigger_onupdate(self):

        val = {'val': 0}

        def callback(value):
            val['val'] = val['val'] + 1

        @jsonclass(class_graph='test_onupdate_0')
        class ClassOne(ORMObject):
            a: str = types.str.required
            b: int = types.int.onupdate(callback).required
        item = ClassOne(a='a', b=1)
        item.a = 'b'
        item._setonsave()
        self.assertEqual(val, {'val': 0})

    def test_orm_objects_if_field_not_modified_do_not_trigger_onupdate(self):

        val = {'val': 0}

        def callback(value):
            val['val'] = val['val'] + 1

        @jsonclass(class_graph='test_onupdate_1')
        class ClassOne(ORMObject):
            a: str = types.str.required
            b: int = types.int.onupdate(callback).required
        item = ClassOne(a='a', b=1)
        setattr(item, "_is_new", False)
        item._setonsave()
        self.assertEqual(val, {'val': 0})

    def test_orm_objects_if_field_modified_trigger_onupdate(self):

        val = {'val': 0}

        def callback(old, new):
            val['val'] = val['val'] + 1 + old + new

        @jsonclass(class_graph='test_onupdate_2')
        class ClassOne(ORMObject):
            a: str = types.str.required
            b: int = types.int.onupdate(callback).required
        item = ClassOne(a='a', b=7)
        setattr(item, "_is_new", False)
        item.b = 8
        item._setonsave()
        self.assertEqual(val, {'val': 16})

    def test_orm_objects_if_other_field_modified_do_not_trigger_onupdate(self):

        val = {'val': 0}

        def callback(value):
            val['val'] = val['val'] + 1

        @jsonclass(class_graph='test_onupdate_3')
        class ClassOne(ORMObject):
            a: str = types.str.required
            b: int = types.int.onupdate(callback).required
        item = ClassOne(a='a', b=1)
        setattr(item, "_is_new", False)
        item.a = 'b'
        item._setonsave()
        self.assertEqual(val, {'val': 0})
