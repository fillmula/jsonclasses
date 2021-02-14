from unittest import TestCase
from datetime import datetime
from jsonclasses import jsonclass, JSONObject, AbstractJSONClassException


class TestAbstractClass(TestCase):

    def test_abstract_class_cannot_be_initialized(self):
        @jsonclass(class_graph='test_abstract_class_1', abstract=True)
        class MyORMObject(JSONObject):
            id: str
            created_at: datetime
            updated_at: datetime
        with self.assertRaises(AbstractJSONClassException) as context:
            MyORMObject()
        self.assertEqual(
            context.exception.message,
            'MyORMObject is an abstract class and should not be initialized')

    def test_non_abstract_class_can_be_initialized(self):
        @jsonclass(class_graph='test_abstract_class_2', abstract=False)
        class MyORMObject(JSONObject):
            id: str
            created_at: datetime
            updated_at: datetime
        MyORMObject()
