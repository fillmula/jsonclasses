import unittest
from jsonclasses import jsonclass, JSONObject


class TestJSONObjectUpdate(unittest.TestCase):

    def test_update_without_arguments_wont_change_anything(self):
        @jsonclass(class_graph='test_update_1')
        class Contact(JSONObject):
            name: str
            address: str
        contact = Contact(name='John', address='Balk')
        contact.update()
        self.assertEqual(contact.__fdict__, {'name': 'John', 'address': 'Balk'})

    def test_update_updates_values_at_given_keys(self):
        @jsonclass(class_graph='test_update_2')
        class Contact(JSONObject):
            name: str
            address: str
        contact = Contact(name='John', address='Balk')
        contact.update(**{'name': 'Peter', 'address': 'Light'})
        self.assertEqual(contact.__fdict__, {'name': 'Peter', 'address': 'Light'})

    def test_update_raises_if_given_key_is_not_allowed(self):
        @jsonclass(class_graph='test_update_3')
        class Contact(JSONObject):
            name: str
            address: str
        contact = Contact(name='John', address='Balk')
        with self.assertRaisesRegex(ValueError, '`nama` not allowed in Contact\\.'):
            contact.update(**{'nama': 'Peter', 'address': 'Light'})

    def test_update_raises_if_given_keys_are_not_allowed(self):
        @jsonclass(class_graph='test_update_4')
        class Contact(JSONObject):
            name: str
            address: str
        contact = Contact(name='John', address='Balk')
        with self.assertRaisesRegex(ValueError, '`.*` not allowed in Contact\\.'):
            contact.update(**{'nama': 'Peter', 'appress': 'Light'})
