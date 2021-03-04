from __future__ import annotations
from unittest import TestCase
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
        self.assertEqual(deadline._data_dict,
                         {'ended_at': '2020-02-04', 'message': None})

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

    def test_update_raises_if_given_key_is_not_allowed(self):
        deadline = SimpleDeadline()
        with self.assertRaises(ValueError) as context:
            deadline.update(**{'name': 'a', 'value': 'b'})
        self.assertRegex(str(context.exception),
                         "'(name|value)', '(value|name)' not allowed in "
                         "SimpleDeadline\\.")
