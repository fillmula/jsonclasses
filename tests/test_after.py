from __future__ import annotations
from datetime import date, datetime
from tests.classes.super_date import SuperDate
from unittest import TestCase
from jsonclasses.excs import ValidationException

class TestAfter(TestCase):

    def test_after_dosent_raise_if_date_value_is_after_date_point(self):
        dad = SuperDate(dad=date(2020, 4, 4))
        dad.validate()

    def test_after_dosent_raise_if_date_value_is_after_datetime_piont(self):
        dadt = SuperDate(dadt=date(2020, 4, 4))
        dadt.validate()

    def test_after_dosent_raise_if_datetime_value_is_after_date_piont(self):
        dtad = SuperDate(dtad=datetime(2020, 4, 4, 12, 30))
        dtad.validate()

    def test_after_raise_if_date_value_and_date_point_are_the_same(self):
        dad = SuperDate(dad=date(2020, 4, 3))
        with self.assertRaises(ValidationException) as context:
            dad.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['dad'],
                         "value is too early")

    def test_after_raise_if_date_value_and_datetime_point_are_the_same(self):
        dadt = SuperDate(dadt=date(2020, 4, 3))
        with self.assertRaises(ValidationException) as context:
            dadt.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['dadt'],
                         "value is too early")

    def test_after_raise_if_datetime_value_and_datetime_point_are_the_same(self):
        dtad = SuperDate(dtad=datetime(2020, 4, 3, 0, 0))
        with self.assertRaises(ValidationException) as context:
            dtad.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['dtad'],
                         "value is too early")


    def test_after_raise_if_date_value_earlier_than_date_point(self):
        dad = SuperDate(dad=date(2020, 4, 2))
        with self.assertRaises(ValidationException) as context:
            dad.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['dad'],
                         "value is too early")

    def test_after_raise_if_date_value_earlier_than_datetime_point(self):
        dadt = SuperDate(dadt=date(2020, 4, 2))
        with self.assertRaises(ValidationException) as context:
            dadt.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['dadt'],
                         "value is too early")

    def test_after_raise_if_datetime_value_earlier_than_date_point(self):
        dtad = SuperDate(dtad=datetime(2020, 4, 2, 0, 0))
        with self.assertRaises(ValidationException) as context:
            dtad.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['dtad'],
                         "value is too early")

    def test_after_does_not_raise_if_date_value_is_after_callable_date_point(self):
        dacd = SuperDate(dacd=date(2020, 4, 4))
        dacd.validate()

    def test_after_does_not_raise_if_date_value_is_after_types_date_piont(self):
        datd = SuperDate(datd=date(2020, 4, 4))
        datd.validate()
