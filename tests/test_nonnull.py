from __future__ import annotations
from unittest import TestCase
from tests.classes.simple_wordbook import SimpleWordbook
from tests.classes.linked_school import LinkedSchool
from tests.classes.linked_student import LinkedStudent
from tests.classes.simple_record import SimpleRecord


class TestNonnull(TestCase):

    def test_nonnull_primitive_list_has_default_value_empty_list(self):
        book = SimpleWordbook(name='Wordbook A')
        self.assertEqual(book.words, [])
        book1 = SimpleWordbook(name='WOrdbook B', words=['tsa', 'mbo'])
        self.assertEqual(book1.words, ['tsa', 'mbo'])

    def test_nonnull_linked_list_has_default_value_empty_list(self):
        school = LinkedSchool(name='School')
        self.assertEqual(school.students, [])
        student = LinkedStudent(name='Student 1')
        school1 = LinkedSchool(name='School 1', students=[student])
        self.assertEqual(school1.students, [student])

    def test_nonnull_dict_has_default_value_empty_dict(self):
        record = SimpleRecord(name='R')
        self.assertEqual(record.dict_record, {})
        record1 = SimpleRecord(name='R', dict_record={'a': '1'})
        self.assertEqual(record1.dict_record, {'a': '1'})

    def test_nonnull_shape_has_default_value_empty_dict(self):
        record = SimpleRecord(name='R')
        self.assertEqual(record.shape_record, {'a': None, 'b': None})
        record1 = SimpleRecord(name='R', shape_record={'a': '3'})
        self.assertEqual(record1.shape_record, {'a': '3', 'b': None})
