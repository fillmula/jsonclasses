from __future__ import annotations
from unittest import TestCase
from datetime import date, datetime
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_deadline import SimpleDeadline


class TestDate(TestCase):

    def test_date_is_date_after_assigned(self):
        deadline = SimpleDeadline(ended_at=date(2020, 11, 20))
        self.assertEqual(deadline._data_dict,
                         {'ended_at': date(2020, 11, 20),
                          'message': None})

    def test_date_converts_datetime_into_date(self):
        deadline = SimpleDeadline(ended_at=datetime(2020, 6, 30, 1, 1, 1))
        self.assertEqual(deadline.ended_at, date(2020, 6, 30))

    def test_datetime_converts_date_str_into_date(self):
        deadline = SimpleDeadline(ended_at='2020-11-20')
        self.assertEqual(deadline.ended_at, date(2020, 11, 20))
        self.assertEqual(type(deadline.ended_at), date)

    def test_datetime_converts_datetime_str_into_date(self):
        deadline = SimpleDeadline(ended_at='2020-11-20T03:03:03.333Z')
        self.assertEqual(deadline.ended_at, date(2020, 11, 20))

    def test_date_raises_if_value_is_not_date(self):
        deadline = SimpleDeadline(ended_at=True)
        with self.assertRaises(ValidationException) as context:
            deadline.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['ended_at'],
                         "Value 'True' at 'ended_at' should be date.")

    def test_date_is_datetime_str_when_tojson(self):
        deadline = SimpleDeadline(ended_at='2020-11-20T03:03:03.333Z')
        self.assertEqual(deadline.tojson(),
                         {'endedAt': '2020-11-20T00:00:00.000Z',
                          'message': None})
