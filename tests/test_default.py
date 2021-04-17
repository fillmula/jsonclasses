from __future__ import annotations
from datetime import datetime, date
from unittest import TestCase
from tests.classes.default_shape import DefaultShape
from tests.classes.simple_order import SimpleOrder
from tests.classes.default_float import DefaultFloat
from tests.classes.simple_book import SimpleBook
from tests.classes.default_date import DefaultDate
from tests.classes.default_datetime import DefaultDatetime
from tests.classes.default_str import DefaultStr
from tests.classes.default_list import DefaultList
from tests.classes.default_dict import DefaultDict
from tests.classes.default_shape_value import DefaultShapeValue
from tests.classes.linked_default_user import LinkedDefaultUser
from tests.classes.linked_default_post import LinkedDefaultPost


class TestDefault(TestCase):

    def test_default_value_appears_in_int(self):
        simple_order = SimpleOrder()
        self.assertEqual(simple_order.quantity, 1)

    def test_default_value_appears_in_float(self):
        default_float = DefaultFloat()
        self.assertEqual(default_float.value, 1.5)

    def test_default_value_appears_in_str(self):
        default_str = DefaultStr()
        self.assertEqual(default_str.value, 'abc')

    def test_default_value_appears_in_bool(self):
        book = SimpleBook()
        self.assertEqual(book.published, False)

    def test_default_value_appears_in_datetime(self):
        default_datetime = DefaultDatetime()
        self.assertEqual(default_datetime.value, datetime(2000, 1, 20, 0, 0))

    def test_default_value_appears_in_date(self):
        default_date = DefaultDate()
        self.assertEqual(default_date.value, date(2000, 1, 20))

    def test_default_value_appears_in_list(self):
        default_list = DefaultList()
        self.assertEqual(default_list.value, ['1', '2', '3'])

    def test_default_value_appears_in_dict(self):
        default_dict = DefaultDict()
        self.assertEqual(default_dict.value, {'a': '1', 'b': '2'})

    def test_default_value_appears_in_shape(self):
        default_shape = DefaultShapeValue()
        self.assertEqual(default_shape.settings,
                         {'ios': False, 'android': True, 'name': 'set'})

    def test_default_value_appears_in_linked_jsonobjects(self):
        user = LinkedDefaultUser(
            posts=[LinkedDefaultPost(), LinkedDefaultPost()])
        self.assertEqual(user.name, 'Default User')
        self.assertEqual(user.posts[0].name, 'Untitled')
        self.assertEqual(user.posts[1].name, 'Untitled')

    def test_nested_default_value_appears_in_shape(self):
        default_shape = DefaultShape(settings={'android': False})
        self.assertEqual(default_shape.settings['ios'], True)
        self.assertEqual(default_shape.settings['android'], False)
        self.assertEqual(default_shape.settings['name'], 'unnamed')
