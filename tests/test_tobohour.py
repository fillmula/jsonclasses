from __future__ import annotations
from datetime import datetime
from unittest import TestCase

from tests.classes.super_datetime import SuperDateTime


class TestTobohour(TestCase):

    def test_tobohour_transforms_datetime_into_the_time_of_beginning_of_hour(self):
        d = SuperDateTime(dtbh=datetime(2021, 10, 11, 17, 37, 27))
        self.assertEqual(d.dtbh, datetime(2021,10, 11, 17, 0))

    def test_tobohour_does_not_transform_if_is_not_datetime(self):
        s = SuperDateTime(stbh="12345")
        self.assertEqual(s.stbh, "12345")
