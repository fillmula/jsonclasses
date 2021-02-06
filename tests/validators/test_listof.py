from unittest import TestCase
from datetime import datetime, date
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException


class TestListOfValidator(TestCase):

    def test_list_validator_throws_if_field_value_is_not_list(self):
        @jsonclass(class_graph='test_listof_1')
        class Book(JSONObject):
            chapters: list[str] = types.listof(types.str).required
        self.assertRaises(ValidationException, Book(chapters='abc').validate)

    def test_list_validator_throws_if_oneof_item_doesnt_match_inner_validator(self):
        @jsonclass(class_graph='test_listof_2')
        class Book(JSONObject):
            chapters: list[str] = types.listof(types.str).required
        book = Book(chapters=['abc', 'def', 'ghi', 4, '789'])
        self.assertRaises(ValidationException, book.validate)

    def test_list_validator_does_not_throw_if_all_items_match_inner_validator(self):
        @jsonclass(class_graph='test_listof_3')
        class Book(JSONObject):
            chapters: list[str] = types.listof(types.str).required
        book = Book(chapters=['abc', 'def', 'ghi', '789'])
        try:
            book.validate()
        except:
            self.fail('list validator should not throw if all items are satisfied.')

    def test_list_validator_accepts_raw_type(self):
        @jsonclass(class_graph='test_listof_4')
        class Book(JSONObject):
            chapters: list[str] = types.listof(str).required
        book = Book(chapters=['abc', 'def', 'ghi', '789'])
        try:
            book.validate()
        except:
            self.fail('list validator should be ok if raw type passes.')

    def test_list_validator_throws_if_given_values_doesnt_match_raw_type(self):
        @jsonclass(class_graph='test_listof_5')
        class Book(JSONObject):
            chapters: list[str] = types.listof(str).required
        book = Book(chapters=['abc', 'def', 'ghi', 5])
        self.assertRaises(ValidationException, book.validate)

    def test_list_validator_transforms_datetime(self):
        @jsonclass(class_graph='test_listof_6')
        class Memory(JSONObject):
            days: list[datetime] = types.listof(datetime).required
        memory = Memory(days=['2020-06-01T02:22:22.222Z', '2020-07-02T02:22:22.222Z'])
        self.assertEqual(memory.days, [
            datetime(2020, 6, 1, 2, 22, 22, 222000),
            datetime(2020, 7, 2, 2, 22, 22, 222000)
        ])

    def test_list_validator_transforms_date(self):
        @jsonclass(class_graph='test_listof_7')
        class Memory(JSONObject):
            days: list[date] = types.listof(date).required
        memory = Memory(days=['2020-06-01T00:00:00.000Z', '2020-07-02T00:00:00.000Z'])
        self.assertEqual(memory.days, [
            date(2020, 6, 1),
            date(2020, 7, 2)
        ])

    def test_listof_convert_datetime_to_json(self):
        @jsonclass(class_graph='test_listof_8')
        class Memory(JSONObject):
            days: list[datetime] = types.listof(datetime).required
        memory = Memory(days=['2020-06-01T02:22:22.222Z', '2020-07-02T02:22:22.222Z'])
        self.assertEqual(memory.tojson(), {
            'days': ['2020-06-01T02:22:22.222Z', '2020-07-02T02:22:22.222Z']
        })

    def test_listof_convert_date_to_json(self):
        @jsonclass(class_graph='test_listof_9')
        class Memory(JSONObject):
            days: list[date] = types.listof(date).required
        memory = Memory(days=['2020-06-01T00:00:00.000Z', '2020-07-02T00:00:00.000Z'])
        self.assertEqual(memory.tojson(), {
            'days': ['2020-06-01T00:00:00.000Z', '2020-07-02T00:00:00.000Z']
        })

    def test_listof_does_not_allow_null_by_default_for_raw_type(self):
        @jsonclass(class_graph='test_listof_10')
        class Quiz(JSONObject):
            numbers: list[int] = types.listof(int)
        quiz = Quiz(numbers=[0, 1, None, 3, 4, 5])
        self.assertRaises(ValidationException, quiz.validate)

    def test_listof_does_not_allow_null_by_default_for_typed_type(self):
        @jsonclass(class_graph='test_listof_11')
        class Quiz(JSONObject):
            numbers: list[int] = types.listof(types.int)
        quiz = Quiz(numbers=[0, 1, None, 3, 4, 5])
        self.assertRaises(ValidationException, quiz.validate)

    def test_listof_does_allow_null_for_typed_type_marked_with_nullable(self):
        @jsonclass(class_graph='test_listof_12')
        class Quiz(JSONObject):
            numbers: list[int] = types.listof(types.int.nullable)
        quiz = Quiz(numbers=[0, 1, None, 3, 4, 5])
        try:
            quiz.validate()
        except:
            self.fail('nullable marked should allow None in list of validator')

    def test_listof_produce_error_messages_for_all_items(self):
        @jsonclass(class_graph='test_listof_13')
        class Quiz(JSONObject):
            numbers: list[int] = types.listof(types.int.min(100))
        quiz = Quiz(numbers=[200, 2, 4, 200, 6, 200])
        self.assertRaisesRegex(ValidationException, 'numbers\\.4', quiz.validate)

    def test_listof_synthesis_types_from_field_type(self):
        @jsonclass(class_graph='test_listof_14')
        class Quiz(JSONObject):
            numbers: list[int]
        quiz = Quiz(numbers=[0, 1, None, 3, 4, 5])
        self.assertRaises(ValidationException, quiz.validate)
