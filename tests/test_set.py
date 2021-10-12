from unittest import TestCase
from datetime import date
from jsonclasses.excs import ValidationException
from tests.classes.simple_book import SimpleBook
from tests.classes.simple_deadline import SimpleDeadline
from tests.classes.simple_article import SimpleArticle
from tests.classes.article import Article
from tests.classes.author import Author
from tests.classes.default_dict import DefaultDict


class TestSet(TestCase):

    def test_set_without_arguments_wont_change_anything(self):
        book = SimpleBook(name='Thao Bvê', published=False)
        book.set()
        self.assertEqual(book._data_dict,
                         {'name': 'Thao Bvê', 'published': False})

    def test_set_with_keyed_arguments_updates_value(self):
        book = SimpleBook(name='Thao Bvê', published=False)
        book.set(name='Thao Boê')
        self.assertEqual(book._data_dict,
                         {'name': 'Thao Boê', 'published': False})

    def test_set_set_multiple_values_at_once(self):
        book = SimpleBook(name='Thao Boê', published=False)
        book.set(name='Thao Bɛ', published=True)
        self.assertEqual(book._data_dict,
                         {'name': 'Thao Bɛ', 'published': True})

    def test_set_returns_self_and_is_chained(self):
        book = SimpleBook(name='Thao Boê', published=False)
        book.set(name='C').set(name='P').set(name='T').set(name='B')
        self.assertEqual(book._data_dict, {'published': False, 'name': 'B'})

    def test_set_triggers_transform(self):
        deadline = SimpleDeadline()
        deadline.set(ended_at='2020-02-04')
        self.assertEqual(
            deadline._data_dict,
            {
                'ended_at': date.fromisoformat('2020-02-04'),
                'message': None
            }
        )

    def test_set_sets_back_value_to_none(self):
        deadline = SimpleDeadline()
        deadline.set(ended_at='2020-02-04').set(ended_at=None)
        self.assertEqual(
            deadline._data_dict,
            {'ended_at': None, 'message': None})

    def test_set_auto_convert_camelcase_keys_into_snakecase(self):
        deadline = SimpleDeadline()
        deadline.set(**{'endedAt': '2020-02-04'})
        self.assertEqual(
            deadline._data_dict,
            {'ended_at': date(2020, 2, 4), 'message': None})

    def test_set_does_not_accept_undefined_keys_by_default(self):
        article = SimpleArticle(title='Ngê Tu Ngê')
        with self.assertRaises(ValidationException) as context:
            article.set(makcêcê='Tu Ngê Dzu Ngê')
        self.assertTrue(len(context.exception.keypath_messages) == 1)
        self.assertEqual(context.exception.keypath_messages['makcêcê'],
                         "key is not allowed")

    def test_set_accepts_object_list(self):
        article = Article(title='Khi Sit', content='Ua Sim Lai Tsa Tiu E Tsai')
        author = Author(name='Hun')
        author.set(articles=[article])
        self.assertEqual(author.articles, [article])

    def test_set_accepts_object(self):
        author = Author(name='Kieng')
        article = Article(title='E Sai',
                          content='Tsê Tioh Si Kim Sieng Ua Ê Tsuê Ai')
        article.set(author=author)
        self.assertEqual(author, article.author)

    def test_set_accepts_nested_keypaths_for_instances(self):
        author = Author(name='Kieng')
        article = Article(**{'title': 'E Sai',
                             'content': 'Tsê Tioh Si Kim Sieng Ua Ê Tsuê Ai',
                             'author': author})
        article.set(**{'author.name': 'abc.def'})
        self.assertEqual(article.author.name, 'abc.def')

    def test_set_accepts_nested_keypaths_for_instances_in_lists(self):
        article = Article(title='T', content='C')
        author = Author(**{'name': 'Kieng', 'articles': [article]})
        author.set(**{'articles.0.title': 'QQQQQ'})
        self.assertEqual(author.articles[0].title, 'QQQQQ')

    def test_set_accepts_nested_keypaths_for_value_in_dicts(self):
        dct = DefaultDict()
        dct.set(**{'value.b': '3', 'value.c': '4'})
        self.assertEqual(dct.value, {'a': '1', 'b': '3', 'c': '4'})

    def test_set_accepts_nested_keypaths_for_value_in_dicts_with_list_indexing(self):
        dct = DefaultDict()
        dct.set(**{'value[b]': '1'})
        self.assertEqual(dct.value, {'a': '1', 'b': '1'})

    def test_set_accepts_nested_keypaths_for_values_in_dicts_with_list_indexing(self):
        dct = DefaultDict()
        dct.set(**{'value[b]': '1', 'value[c]': '2'})
        self.assertEqual(dct.value, {'a': '1', 'b': '1', 'c': '2'})

    def test_set_accepts_nested_keypaths_for_instances_with_list_indexing(self):
        author = Author(name='Kieng')
        article = Article(**{'title': 'E Sai',
                             'content': 'Tsê Tioh Si Kim Sieng Ua Ê Tsuê Ai',
                             'author': author})
        article.set(**{'author[name]': 'abca.def'})
        self.assertEqual(article.author.name, 'abca.def')

    def test_set_accepts_nested_keypaths_for_instances_with_multiple_list_indexing(self):
        article = Article(title='T', content='C')
        author = Author(**{'name': 'Kieng', 'articles': [article]})
        author.set(**{'articles[0][title]': 'QQQQQ'})
        self.assertEqual(author.articles[0].title, 'QQQQQ')
