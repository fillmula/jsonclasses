from unittest import TestCase
from typing import Optional
from jsonclasses import jsonclass, JSONObject, ValidationException, types
from datetime import datetime, date


class TestJSONObjectInitialize(TestCase):

    def test_initialize_without_arguments(self):
        @jsonclass(class_graph='test_initialize_1')
        class Contact(JSONObject):
            name: str
            address: str
        contact = Contact()
        self.assertEqual(contact.__fdict__, {'name': None, 'address': None})
