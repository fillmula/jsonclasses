from __future__ import annotations
from unittest import TestCase
from jsonclasses import jsonclass
from tests.classes.simple_book import SimpleBook
from tests.classes.simple_deadline import SimpleDeadline


class TestUpdate(TestCase):

    def test_update_without_arguments_wont_change_anything(self):
        book = SimpleBook(name='Thao Bvê', published=False)
        book.update()
        self.assertEqual(book._data_dict,
                         {'name': 'Thao Bvê', 'published': False})

    def test_update_with_keyed_arguments_updates_value(self):
        book = SimpleBook(name='Thao Bvê', published=False)
        book.update(name='Thao Boê')
        self.assertEqual(book._data_dict,
                         {'name': 'Thao Boê', 'published': False})

    def test_update_set_multiple_values_at_once(self):
        book = SimpleBook(name='Thao Boê', published=False)
        book.update(name='Thao Bɛ', published=True)
        self.assertEqual(book._data_dict,
                         {'name': 'Thao Bɛ', 'published': True})

    def test_update_returns_self_and_is_chained(self):
        book = SimpleBook(name='Thao Boê', published=False)
        book.update(name='C').update(name='P') \
            .update(name='T').update(name='B')
        self.assertEqual(book._data_dict, {'published': False, 'name': 'B'})

    def test_update_does_not_trigger_transform(self):
        deadline = SimpleDeadline()
        deadline.update(ended_at='2020-02-04')
        self.assertEqual(
            deadline._data_dict,
            {
                'ended_at': '2020-02-04',
                'message': None
            }
        )

    def test_update_sets_back_value_to_none(self):
        deadline = SimpleDeadline()
        deadline.update(ended_at='2020-02-04').update(ended_at=None)
        self.assertEqual(
            deadline._data_dict,
            {'ended_at': None, 'message': None})

    def test_update_does_not_auto_convert_camelcase_keys_into_snakecase(self):
        deadline = SimpleDeadline()
        with self.assertRaises(ValueError):
            deadline.update(**{'endedAt': '2020-02-04'})

    # def test_update_raises_if_given_key_is_not_allowed(self):
    #     @jsonclass(class_graph='test_update_3')
    #     class Contact(JSONObject):
    #         name: str
    #         address: str
    #     contact = Contact(name='John', address='Balk')
    #     with self.assertRaisesRegex(ValueError, '`nama` not allowed in Contact\\.'):
    #         contact.update(**{'nama': 'Peter', 'address': 'Light'})

    # def test_update_raises_if_given_keys_are_not_allowed(self):
    #     @jsonclass(class_graph='test_update_4')
    #     class Contact(JSONObject):
    #         name: str
    #         address: str
    #     contact = Contact(name='John', address='Balk')
    #     with self.assertRaisesRegex(ValueError, '`.*` not allowed in Contact\\.'):
    #         contact.update(**{'nama': 'Peter', 'appress': 'Light'})
