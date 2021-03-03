from unittest import TestCase
from jsonclasses import jsonclass, JSONObject, JSONEncoder
from json import dumps


class TestJSONObjectInitialize(TestCase):

    def test_json_encoder_encodes_str(self):
        @jsonclass(class_graph='test_json_encoder_1')
        class Contact(JSONObject):
            name: str
            address: str
        contact = Contact(name='John', address='Stanley Road')
        json_str = dumps(contact, cls=JSONEncoder)
        self.assertEqual(json_str, '{"name": "John", "address": "Stanley Road"}')

    def test_json_encoder_encodes_list(self):
        @jsonclass(class_graph='test_json_encoder_2')
        class Contact(JSONObject):
            name: str
            address: str
        contact1 = Contact(name='John', address='Stanley Road')
        contact2 = Contact(name='Peter', address='Paterson Road')
        json_str = dumps([contact1, contact2], cls=JSONEncoder)
        self.assertEqual(
            json_str,
            '[{"name": "John", "address": "Stanley Road"}, {"name": "Peter", "address": "Paterson Road"}]'
        )
