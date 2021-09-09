from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.simple_record import SimpleRecord
from tests.classes.typed_record import TypedRecord
from tests.classes.nullable_record import NullableRecord
from tests.classes.simple_weather import CamelizedWeather, UncamelizedWeather
from tests.classes.simple_quiz import SimpleQuiz


class TestDictOf(TestCase):

    def test_dictof_raises_if_value_is_not_dict(self):
        record = SimpleRecord(dict_record=5)
        self.assertRaises(ValidationException, record.validate)

    def test_dictof_raises_if_one_of_values_does_not_match_inner(self):
        record = SimpleRecord(dict_record={'a': '1', 'b': 2})
        self.assertRaises(ValidationException, record.validate)

    def test_dictof_does_not_raise_if_all_values_match_inner(self):
        record = SimpleRecord(dict_record={'a': '1', 'b': '2'})
        record.validate()

    def test_dictof_accepts_raw_type(self):
        record = SimpleRecord(dict_record={'a': '1', 'b': '2'})
        record.validate()
        record1 = SimpleRecord(dict_record={'a': '1', 'b': 2})
        self.assertRaises(ValidationException, record1.validate)

    def test_dictof_accepts_types_type(self):
        record = TypedRecord(dict_record={'a': '1', 'b': '2'})
        record.validate()
        record1 = TypedRecord(dict_record={'a': '1', 'b': 2})
        self.assertRaises(ValidationException, record1.validate)

    def test_dictof_does_not_allow_none_for_raw_typed_dict(self):
        record1 = SimpleRecord(dict_record={'a': '1', 'b': None})
        self.assertRaises(ValidationException, record1.validate)

    def test_dictof_does_not_allow_none_for_types_typed_dict(self):
        record1 = TypedRecord(dict_record={'a': '1', 'b': None})
        self.assertRaises(ValidationException, record1.validate)

    def test_dictof_allow_none_for_nullable_marked_typed_dict(self):
        record1 = NullableRecord(dict_record={'a': '1', 'b': None})
        record1.validate()

    def test_dictof_keep_keys_on_init(self):
        weather = CamelizedWeather(data={'lastDay': '2', 'nextDay': '4'})
        self.assertEqual(weather.data, {'lastDay': '2', 'nextDay': '4'})

    def test_dictof_keep_keys_on_tojson(self):
        weather = CamelizedWeather(data={'lastDay': '2', 'nextDay': '4'})
        self.assertEqual(weather.tojson()['data'],
                         {'lastDay': '2', 'nextDay': '4'})

    def test_dictof_validate_raises_for_one_item(self):
        quiz = SimpleQuiz(numbers={'a': 200,
                                   'b': 2,
                                   'c': 4,
                                   'd': 200,
                                   'e': 6,
                                   'f': 200})
        with self.assertRaises(ValidationException) as context:
            quiz.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['numbers.b'],
                         "value is not greater than or equal 100")
