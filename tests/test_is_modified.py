from __future__ import annotations
from unittest import TestCase
from tests.classes.simple_order import SimpleOrder
from tests.classes.simple_project import SimpleProject
from tests.classes.simple_chart import SimpleChart
from tests.classes.author import Author
from tests.classes.nested_object import NestedDict, NestedList
from tests.classes.linked_song import LinkedSong, LinkedSinger


class TestIsModified(TestCase):

    def test_jobject_is_not_modified_by_default(self):
        order = SimpleOrder(quantity=5)
        order._mark_not_new()
        self.assertEqual(order.is_modified, False)

    def test_jobject_is_modified_is_readonly(self):
        order = SimpleOrder(quantity=5)
        with self.assertRaises(AttributeError) as context:
            order.is_modified = True
        self.assertEqual(str(context.exception), "can't set attribute")

    def test_jobject_is_modified_if_any_field_is_modified(self):
        order = SimpleOrder(quantity=5)
        order._mark_not_new()
        order.quantity = 2
        self.assertEqual(order.modified_fields, ('quantity',))
        self.assertEqual(order.is_modified, True)

    def test_jobject_is_modified_if_list_value_is_mutated(self):
        project = SimpleProject(name='OK', attendees=['Butai', 'Buti'])
        project._mark_not_new()
        project.attendees.append('Liittiengesai')
        self.assertEqual(project.modified_fields, ('attendees',))
        self.assertEqual(project.is_modified, True)

    def test_jobject_is_modified_if_dict_value_is_mutated(self):
        chart = SimpleChart(name='B', partitions={'thenha': 0.5, 'guaê': 0.3})
        chart._mark_not_new()
        chart.partitions['lanê'] = 0.8
        self.assertEqual(chart.modified_fields, ('partitions',))
        self.assertEqual(chart.is_modified, True)

    def test_jobject_is_not_modified_if_nested_is_mutated(self):
        author = Author(name='Kia',
                        articles=[{'title': 'Long',
                                   'content': 'Khng Ti Ua E Sim Lai'}])
        author._mark_not_new()
        author.articles[0]._mark_not_new()
        author.articles[0].title = 'M Guan Kong Tsai Huê'
        self.assertEqual(author.is_modified, False)
        self.assertEqual(author.modified_fields, ())
        self.assertEqual(author.articles[0].is_modified, True)
        self.assertEqual(author.articles[0].modified_fields, ('title',))

    def test_jobject_is_modified_if_nested_list_is_modified(self):
        nlst = NestedList(id='1', value={'a': ['1', '2'], 'b': ['1', '2']})
        nlst._mark_not_new()
        nlst.value['b'].append('3')
        self.assertEqual(nlst.is_modified, True)
        self.assertEqual(nlst.modified_fields, ('value.b',))

    def test_jobject_is_modified_if_nested_dict_is_modified(self):
        ndct = NestedDict(id='1', value=[{'a': '1'}, {'b': '1'}])
        ndct._mark_not_new()
        ndct.value[1]['c'] = '2'
        self.assertEqual(ndct.is_modified, True)
        self.assertEqual(ndct.modified_fields, ('value.1',))

    def test_jobject_is_modified_if_local_key_list_is_assigned(self):
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        song = LinkedSong(id=1, singers=[singer1, singer2])
        song._mark_not_new()
        self.assertEqual(song.is_modified, False)
        song.singer_ids = [3, 4]
        self.assertEqual(song.is_modified, True)
        self.assertEqual(song.modified_fields, ('singers',))

    def test_jobject_is_modified_if_local_key_list_is_assigned_nothing_changed_to_object_list(self):
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        song = LinkedSong(id=1, singers=[singer1, singer2])
        song._mark_not_new()
        self.assertEqual(song.is_modified, False)
        song.singer_ids = [1, 2, 3]
        self.assertEqual(song.is_modified, True)
        self.assertEqual(song.modified_fields, ('singers',))


    def test_jobject_is_modified_if_local_key_list_is_appended(self):
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        song = LinkedSong(id=1, singers=[singer1, singer2])
        song._mark_not_new()
        self.assertEqual(song.is_modified, False)
        song.singer_ids.append(3)
        self.assertEqual(song.is_modified, True)
        self.assertEqual(song.modified_fields, ('singers',))

    def test_jobject_is_modified_if_local_key_list_is_truncated(self):
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        song = LinkedSong(id=1, singers=[singer1, singer2])
        song._mark_not_new()
        self.assertEqual(song.is_modified, False)
        song.singer_ids.remove(2)
        self.assertEqual(song.singers, [singer1])
        self.assertEqual(song.is_modified, True)
        self.assertEqual(song.modified_fields, ('singers',))

    def test_jobject_is_modified_if_local_key_list_is_truncated_nothing_changed_to_object_list(self):
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        song = LinkedSong(id=1, singers=[singer1, singer2])
        song.singer_ids.append(5)
        song._mark_not_new()
        self.assertEqual(song.is_modified, False)
        song.singer_ids.remove(5)
        self.assertEqual(song.singers, [singer1, singer2])
        self.assertEqual(song.is_modified, True)
        self.assertEqual(song.modified_fields, ('singers',))


    def test_jobject_is_modified_if_local_key_field_list_is_assigned(self):
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        singer3 = LinkedSinger(id=3)
        song = LinkedSong(id=1, singers=[singer1, singer2])
        song._mark_not_new()
        self.assertEqual(song.is_modified, False)
        song.singers = [singer1, singer2, singer3]
        self.assertEqual(song.is_modified, True)
        self.assertEqual(song.modified_fields, ('singers',))

    def test_jobject_is_not_modified_if_local_key_field_list_is_assigned_nothing_changed_at_all(self):
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        song = LinkedSong(id=1, singers=[singer1, singer2])
        song._mark_not_new()
        self.assertEqual(song.is_modified, False)
        song.singers = [singer1, singer2]
        self.assertEqual(song.is_modified, False)
        self.assertEqual(song.modified_fields, ())

    def test_jobject_is_modified_if_local_key_field_list_is_appended(self):
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        singer3 = LinkedSinger(id=3)
        song = LinkedSong(id=1, singers=[singer1, singer2])
        song._mark_not_new()
        self.assertEqual(song.is_modified, False)
        song.singers.append(singer3)
        self.assertEqual(song.is_modified, True)
        self.assertEqual(song.modified_fields, ('singers',))

    def test_jobject_is_modified_if_local_key_field_list_is_truncated(self):
        singer1 = LinkedSinger(id=1)
        singer2 = LinkedSinger(id=2)
        singer3 = LinkedSinger(id=3)
        song = LinkedSong(id=1, singers=[singer1, singer2, singer3])
        song._mark_not_new()
        self.assertEqual(song.is_modified, False)
        song.singers.remove(singer3)
        self.assertEqual(song.is_modified, True)
        self.assertEqual(song.modified_fields, ('singers',))
