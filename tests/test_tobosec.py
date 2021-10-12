from __future__ import annotations
from datetime import datetime
from unittest import TestCase
from tests.classes.super_datetime import SuperDateTime

class TestTobosec(TestCase):

    def test_tobosec_transforms_datetime_into_the_time_of_beginning_of_second(self):
        d = SuperDateTime(dtbs=datetime(2021, 10, 11, 17, 37, 27, 446259))
        self.assertEqual(d.dtbs, datetime(2021,10, 11, 17, 37, 27))

    def test_tobosec_does_not_transform_if_is_not_datetime(self):
        s = SuperDateTime(stbs="12345")
        self.assertEqual(s.stbs, "12345")
