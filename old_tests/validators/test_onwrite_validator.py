from __future__ import annotations
from unittest import TestCase
from jsonclasses import jsonclass, ORMObject, types


class TestOnWriteVailidator(TestCase):

    def test_orm_objects_if_new_triggers_on_write(self):

        val = {'val': 0}

        def callback(value):
            val['val'] = val['val'] + 1

        @jsonclass(class_graph='test_onwrite_0')
        class ClassOne(ORMObject):
            a: str = types.str.required
            b: int = types.int.onwrite(callback).required
        item = ClassOne(a='a', b=1)
        item.a = 'b'
        item._setonsave()
        self.assertEqual(val, {'val': 1})
        self.assertEqual(item.b, 1)

    def test_orm_objects_if_only_other_field_modified_do_not_trigger_onwrite(self):
        val = {'val': 0}

        def callback(value):
            val['val'] = val['val'] + 1

        @jsonclass(class_graph='test_onwrite_1')
        class ClassOne(ORMObject):
            a: str = types.str.required
            b: int = types.int.onwrite(callback).required
        item = ClassOne(a='a', b=1)
        setattr(item, '_is_new', False)
        item.a = 'b'
        item._setonsave()
        self.assertEqual(val, {'val': 0})
        self.assertEqual(item.b, 1)

    def test_orm_objects_if_field_modified_trigger_onwrite(self):
        val = {'val': 0}

        def callback(value):
            val['val'] = val['val'] + 1
            val['value'] = value

        @jsonclass(class_graph='test_onwrite_2')
        class ClassOne(ORMObject):
            a: str = types.str.required
            b: int = types.int.onwrite(callback).required
        item = ClassOne(a='a', b=1)
        setattr(item, '_is_new', False)
        item.b = 5
        item._setonsave()
        self.assertEqual(val, {'val': 1, 'value': 5})
