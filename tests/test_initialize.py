from __future__ import annotations
from unittest import TestCase
from datetime import date
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_article import SimpleArticle
from tests.classes.simple_order import SimpleOrder
from tests.classes.simple_address import SimpleAddress
from tests.classes.simple_student import SimpleStudent
from tests.classes.simple_deadline import SimpleDeadline
from tests.classes.author import Author
from tests.classes.article import Article
from tests.classes.default_shape import DefaultShape
from tests.classes.nest_shape_user import NestShapeUser
from tests.classes.default_dict import DefaultDict


class TestInitialize(TestCase):

    def test_initialize_simple_object_without_arguments(self):
        article = SimpleArticle()
        self.assertEqual(article._data_dict, {'title': None, 'content': None})

    def test_initialize_simple_object_with_arguments(self):
        article = SimpleArticle(title='Oi', content='Tik')
        self.assertEqual(article._data_dict, {'title': 'Oi', 'content': 'Tik'})

    def test_initialize_simple_object_with_types_default_values(self):
        order = SimpleOrder(name='Oi Tik')
        self.assertEqual(order._data_dict, {'name': 'Oi Tik', 'quantity': 1})

    def test_initialize_simple_object_with_assigned_default_values(self):
        student = SimpleStudent()
        self.assertEqual(student._data_dict, {'age': 20, 'graduated': False})

    def test_initialize_with_value_passed_in_rather_than_default_value(self):
        student = SimpleStudent(graduated=True, age=24)
        self.assertEqual(student._data_dict, {'age': 24, 'graduated': True})

    def test_initialize_do_not_accept_undefined_keys_by_default(self):
        with self.assertRaises(ValidationException) as context:
            SimpleArticle(dzimsikai='Ku Piang Hoê')
        self.assertTrue(len(context.exception.keypath_messages) == 1)
        print("ERRMSG: ", context.exception.keypath_messages)
        self.assertEqual(context.exception.keypath_messages['dzimsikai'],
                         "Key 'dzimsikai' is not allowed.")

    def test_initialize_underscore_key_cases_by_default(self):
        address = SimpleAddress(**{'lineOne': 'NgouOu', 'lineTwo': 'Sihai'})
        self.assertEqual(address._data_dict,
                         {'line_one': 'NgouOu', 'line_two': 'Sihai'})

    def test_initialize_triggers_transform(self):
        deadline = SimpleDeadline(ended_at='2021-06-30')
        self.assertEqual(deadline.ended_at, date(2021, 6, 30))

    def test_initialize_accepts_object_list(self):
        article = Article(title='Khi Sit', content='Ua Sim Lai Tsa Tiu E Tsai')
        author = Author(name='Hun', articles=[article])
        self.assertEqual(author.articles, [article])

    def test_initialize_accepts_object(self):
        author = Author(name='Kieng')
        article = Article(title='E Sai',
                          content='Tsê Tioh Si Kim Sieng Ua Ê Tsuê Ai',
                          author=author)
        self.assertEqual(author, article.author)

    def test_initialize_accepts_nested_keypaths_for_nonnull_shape(self):
        shape = DefaultShape(**{'settings.ios': False, 'settings.name': 'equal'})
        self.assertEqual(shape.settings.ios, False)
        self.assertEqual(shape.settings.name, 'equal')

    def test_initialize_accepts_nested_keypaths_for_instances(self):
        author = Author(name='Kieng')
        article = Article(**{'title': 'E Sai',
                             'content': 'Tsê Tioh Si Kim Sieng Ua Ê Tsuê Ai',
                             'author': author,
                             'author.name': 'abc.def'})
        self.assertEqual(article.author.name, 'abc.def')

    def test_initialize_accepts_nested_keypaths_for_instances_in_lists(self):
        article = Article(title='T', content='C')
        author = Author(**{'name': 'Kieng', 'articles': [article], 'articles.0.title': 'QQQQQ'})
        self.assertEqual(author.articles[0].title, 'QQQQQ')

    def test_initialize_accepts_nested_keypaths_for_shape_in_shape(self):
        user = NestShapeUser(**{'name': 'N', 'grouped': {
            'ios': {'on': True, 'off': False},
            'android': {'on': False, 'off': True}
        }, 'grouped.ios.on': False, 'grouped.ios.off': True})
        self.assertEqual(user.grouped.ios['on'], False)
        self.assertEqual(user.grouped.ios['off'], True) # TODO: use dot notation

    def test_initialize_accepts_nested_keypaths_for_value_in_dicts(self):
        dct = DefaultDict(**{'value.b': '3', 'value.c': '4'})
        self.assertEqual(dct.value, {'a': '1', 'b': '3', 'c': '4'})
