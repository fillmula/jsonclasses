from __future__ import annotations
from unittest import TestCase
from datetime import date, datetime
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_balance import SimpleBalance


class TestDatetime(TestCase):

    def test_datetime_is_datetime_after_assigned(self):
        balance = SimpleBalance(date=datetime(2020, 11, 20, 0, 0, 1))
        self.assertEqual(balance._data_dict,
                         {'date': datetime(2020, 11, 20, 0, 0, 1),
                          'balance': None})

    def test_datetime_converts_date_into_datetime(self):
        balance = SimpleBalance(date=date(2020, 6, 30))
        self.assertEqual(balance.date, datetime(2020, 6, 30, 0, 0, 0))

    def test_datetime_converts_date_str_into_datetime(self):
        balance = SimpleBalance(date='2020-11-20')
        self.assertEqual(balance.date, datetime(2020, 11, 20, 0, 0, 0))
        self.assertEqual(type(balance.date), datetime)

    def test_datetime_converts_datetime_str_into_datetime(self):
        balance = SimpleBalance(date='2020-11-20T03:03:03.333Z')
        self.assertEqual(balance.date, datetime(2020, 11, 20, 3, 3, 3, 333000))

    def test_datetime_raises_if_value_is_not_datetime(self):
        balance = SimpleBalance(date=True)
        with self.assertRaises(ValidationException) as context:
            balance.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['date'],
                         "Value 'True' at 'date' should be datetime.")

    def test_datetime_is_datetime_str_when_tojson(self):
        balance = SimpleBalance(date='2020-11-20T03:03:03.333Z')
        self.assertEqual(balance.tojson(),
                         {'date': '2020-11-20T03:03:03.333Z', 'balance': None})
