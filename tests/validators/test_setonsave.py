from __future__ import annotations
from jsonclasses.orm_object import ORMObject
from unittest import TestCase
from jsonclasses import (jsonclass, JSONObject, ORMObject, types,
                         ValidationException)


class TestSetOnSaveVailidator(TestCase):

    def test_orm_objects_if_modified_trigger_setonsave(self):
        @jsonclass(class_graph='test_setonsave_1')
        class ClassOne(ORMObject):
            a: str = types.str.required
            b: int = types.int.setonsave(lambda x: x + 1).required
        item = ClassOne(a='a', b=1)
        setattr(item, '_is_new', False)
        item.a = 'b'
        item._setonsave()
        self.assertEqual(item.a, 'b')
        self.assertEqual(item.b, 2)
