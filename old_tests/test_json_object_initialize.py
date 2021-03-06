import unittest
from typing import Optional
from jsonclasses import jsonclass, JSONObject, ValidationException, types
from datetime import datetime, date


class TestJSONObjectInitialize(unittest.TestCase):

    def test_initialize_strict_raises_on_nested_unallowed_keys(self):
        @jsonclass(class_graph='test_initialize_16', strict_input=True)
        class Friend(JSONObject):
            name: str

        @jsonclass(class_graph='test_initialize_16', strict_input=True)
        class User(JSONObject):
            friends: list[Friend]

        with self.assertRaisesRegex(ValidationException, "'friends.0.age': Key 'age' at 'friends.0' is not allowed."):
            User(**{'friends': [{'name': 'John', 'age': 15}]})

    def test_initialize_strict_handle_correctly_for_multiple_inheritance(self):
        @jsonclass(class_graph='test_initialize_17', strict_input=True)
        class BaseObject(JSONObject):
            pass

        @jsonclass(class_graph='test_initialize_17', strict_input=True)
        class DBObject(BaseObject):
            id: str = (types.str.readonly.primary.default(lambda: str())
                       .required)
            created_at: datetime = (types.datetime.readonly.timestamp('created')
                                    .default(datetime.now).required)
            updated_at: datetime = (types.datetime.readonly.timestamp('updated')
                                    .default(datetime.now).setonsave(datetime.now)
                                    .required)
            deleted_at: Optional[datetime] = (types.datetime.readonly
                                              .timestamp('deleted'))

        @jsonclass(class_graph='test_initialize_17', strict_input=True)
        class MyObject(DBObject):
            name: str
            age: int

        input = {'name': 'John', 'age': 27}
        MyObject(**input)
