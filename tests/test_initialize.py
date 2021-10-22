from __future__ import annotations
from datetime import date
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.simple_article import SimpleArticle
from tests.classes.simple_order import SimpleOrder
from tests.classes.simple_address import SimpleAddress
from tests.classes.simple_student import SimpleStudent
from tests.classes.simple_deadline import SimpleDeadline
from tests.classes.author import Author
from tests.classes.article import Article
from tests.classes.default_dict import DefaultDict
from tests.classes.linked_song import LinkedSong, LinkedSinger


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
        self.assertEqual(context.exception.keypath_messages['dzimsikai'],
                         "key is not allowed")

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

    def test_initialize_accepts_nested_keypaths_for_value_in_dicts(self):
        dct = DefaultDict(**{'value.b': '3', 'value.c': '4'})
        self.assertEqual(dct.value, {'a': '1', 'b': '3', 'c': '4'})

    def test_initialized_object_list_local_keys_can_be_accessed(self):
        song = LinkedSong()
        self.assertEqual(song.singers, [])
        self.assertEqual(song.singer_ids, [])

    def test_initialized_object_list_add_local_object_syncs_local_key(self):
        song = LinkedSong(id=1)
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        song.singers = [singer1]
        self.assertEqual(song.singer_ids, [1])
        song.singers.append(singer2)
        self.assertEqual(song.singer_ids, [1, 2])

    def test_initialized_object_list_del_local_object_syncs_local_key(self):
        song = LinkedSong(id=1)
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        song.singers = [singer1]
        self.assertEqual(song.singer_ids, [1])
        song.singers.append(singer2)
        self.assertEqual(song.singer_ids, [1, 2])
        song.singers.remove(singer2)
        self.assertEqual(song.singer_ids, [1])

    def test_initialized_object_list_assign_local_object_syncs_local_key(self):
        song = LinkedSong(id=1)
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        singer3 = LinkedSinger(id=3)
        singer4 = LinkedSinger(id=4)
        song.singers = [singer1]
        self.assertEqual(song.singer_ids, [1])
        song.singers.append(singer2)
        self.assertEqual(song.singer_ids, [1, 2])
        song.singers = [singer3, singer4]
        self.assertEqual(song.singer_ids, [3, 4])
        self.assertEqual(song.singers, [singer3, singer4])

    def test_initialized_object_list_add_local_key_syncs_local_object(self):
        song = LinkedSong(id=1)
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        song.singers = [singer1, singer2]
        song.singer_ids.append(3)
        self.assertEqual(song.singers, [singer1, singer2])

    def test_initialized_object_list_del_local_key_syncs_local_object(self):
        song = LinkedSong(id=1)
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        song.singers = [singer1, singer2]
        self.assertEqual(singer2.songs, [song])
        song.singer_ids.remove(2)
        self.assertEqual(song.singers, [singer1])
        self.assertEqual(singer2.songs, [])

    def test_initialized_object_list_assign_local_key_syncs_local_object(self):
        song = LinkedSong(id=1)
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        singer3 = LinkedSinger(id=3)
        singer4 = LinkedSinger(id=4)
        song.singers = [singer1]
        self.assertEqual(song.singer_ids, [1])
        song.singer_ids = [7, 8, 1, 9, 10]
        self.assertEqual(song.singers, [singer1])
        self.assertEqual(song.singer_ids, [7, 8, 1, 9, 10])
