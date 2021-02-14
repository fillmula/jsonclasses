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

    def test_abstract_classs_non_abstract_subclass_can_be_initialized(self):
        @jsonclass(class_graph='test_abstract_class_3', abstract=True)
        class MyORMObject(JSONObject):
            id: str
            created_at: datetime
            updated_at: datetime

        @jsonclass(class_graph='test_abstract_class_3')
        class MyObject(MyORMObject):
            name: str
        MyObject()

    def test_abstract_class_class_is_not_abstract_by_default(self):
        @jsonclass(class_graph='test_abstract_class_4')
        class MyORMObject(JSONObject):
            id: str
            created_at: datetime
            updated_at: datetime
        MyORMObject()
