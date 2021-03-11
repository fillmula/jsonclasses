from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_list import SimpleList
from tests.classes.typed_list import TypedList
from tests.classes.list_quiz import ListQuiz
from tests.classes.nullable_list import NullableList


class TestListOf(TestCase):

    def test_listof_raises_if_value_is_not_list(self):
        slst = SimpleList(list=5)
        self.assertRaises(ValidationException, slst.validate)

    def test_listof_raises_if_one_of_values_does_not_match_inner(self):
        slst = SimpleList(list=[5, 4, 3, 2, 1.5])
        self.assertRaises(ValidationException, slst.validate)

    def test_listof_does_not_raise_if_all_values_match_inner(self):
        slst = SimpleList(list=[5, 4, 3, 2, 1])
        slst.validate()

    def test_listof_accepts_raw_type(self):
        slst = SimpleList(list=[5, 4, 3, 2, 1.5])
        self.assertRaises(ValidationException, slst.validate)
        slst1 = SimpleList(list=[5, 4, 3, 2, 1])
        slst1.validate()

    def test_listof_accepts_types_type(self):
        slst = TypedList(list=[5, 4, 3, 2, 1.5])
        self.assertRaises(ValidationException, slst.validate)
        slst1 = TypedList(list=[5, 4, 3, 2, 1])
        slst1.validate()

    def test_listof_does_not_allow_none_for_raw_typed_list(self):
        record1 = SimpleList(list=[5, 4, None])
        self.assertRaises(ValidationException, record1.validate)

    def test_listof_does_not_allow_none_for_types_typed_list(self):
        record1 = TypedList(list=[5, 4, None])
        self.assertRaises(ValidationException, record1.validate)

    def test_listof_allow_none_for_nullable_marked_typed_list(self):
        record1 = NullableList(list=[5, 4, None])
        record1.validate()

    def test_listof_validate_raises_for_one_item(self):
        quiz = ListQuiz(numbers=[200, 2, 4, 200, 6, 200])
        with self.assertRaises(ValidationException) as context:
            quiz.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['numbers.1'],
                         "Value '2' at 'numbers.1' should not be less than "
                         "100.")
