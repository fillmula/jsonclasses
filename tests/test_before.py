from __future__ import annotations
from datetime import date, datetime
from tests.classes.super_date import SuperDate
from unittest import TestCase
from jsonclasses.excs import ValidationException

class TestBefore(TestCase):

    def test_before_does_not_raise_if_date_value_is_before_date_point(self):
        dbd = SuperDate(dbd=date(2020, 4, 2))
        dbd.validate()

    def test_before_does_not_raise_if_date_value_is_before_datetime_piont(self):
        dbdt = SuperDate(dbdt=date(2020, 4, 2))
        dbdt.validate()

    def test_before_does_not_raise_if_datetime_value_is_before_date_piont(self):
        dtbd = SuperDate(dtbd=datetime(2020, 4, 2, 12, 30))
        dtbd.validate()

    def test_before_raise_if_date_value_and_date_point_are_the_same(self):
        dbd = SuperDate(dbd=date(2020, 4, 3))
        with self.assertRaises(ValidationException) as context:
            dbd.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['dbd'],
                         "value is too late")

    def test_before_raise_if_date_value_and_datetime_point_are_the_same(self):
        dbdt = SuperDate(dbdt=date(2020, 4, 3))
        with self.assertRaises(ValidationException) as context:
            dbdt.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['dbdt'],
                         "value is too late")

    def test_before_raise_if_datetime_value_and_datetime_point_are_the_same(self):
        dtbd = SuperDate(dtbd=datetime(2020, 4, 3, 0, 0))
        with self.assertRaises(ValidationException) as context:
            dtbd.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['dtbd'],
                         "value is too late")


    def test_before_raise_if_date_value_later_than_date_point(self):
        dbd = SuperDate(dbd=date(2020, 4, 4))
        with self.assertRaises(ValidationException) as context:
            dbd.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['dbd'],
                         "value is too late")

    def test_before_raise_if_date_value_later_than_datetime_point(self):
        dbdt = SuperDate(dbdt=date(2020, 4, 4))
        with self.assertRaises(ValidationException) as context:
            dbdt.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['dbdt'],
                         "value is too late")

    def test_before_raise_if_datetime_value_later_than_date_point(self):
        dtbd = SuperDate(dtbd=datetime(2020, 4, 4, 0, 0))
        with self.assertRaises(ValidationException) as context:
            dtbd.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['dtbd'],
                         "value is too late")

    def test_before_does_not_raise_if_date_value_is_before_callable_date_point(self):
        dbcd = SuperDate(dbcd=date(2020, 4, 2))
        dbcd.validate()

    def test_before_does_not_raise_if_date_value_is_before_types_date_piont(self):
        dbtd = SuperDate(dbtd=date(2020, 4, 2))
        dbtd.validate()
