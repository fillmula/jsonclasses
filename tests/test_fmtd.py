from __future__ import annotations
from datetime import date, datetime
from tests.classes.simple_datetime import SimpleDatetime
from unittest import TestCase

class TestFormatDatetime(TestCase):

    def test_fmtd_formats_datetime_value(self):
        dt = SimpleDatetime(fmtdt=datetime(2021, 3, 3, 12, 12, 12))
        self.assertEqual(dt.tojson()['fmtdt'],"2021年03月03日 12:12:12")

    def test_fmtd_formats_date_value(self):
        d = SimpleDatetime(fmtd=date(2021, 3, 3))
        self.assertEqual(d.tojson()['fmtd'], "2021年03月03日")

    def test_fmtd_formats_datetime_str_value(self):
        dts = SimpleDatetime(fmtdts="2021-11-20T03:03:03.333Z")
        self.assertEqual(dts.tojson()['fmtdts'], "2021年11月20日 03:03:03")

    def test_fmtd_formats_date_str_value(self):
        ds = SimpleDatetime(fmtds="2021-11-20")
        self.assertEqual(ds.tojson()['fmtds'], "2021年11月20日")

    def test_fmtd_formats_datetime_value_with_callable_format_str(self):
        dt = SimpleDatetime(cfmtdt=datetime(2021, 3, 3, 12, 12, 12))
        self.assertEqual(dt.tojson()['cfmtdt'],"2021年03月03日 12:12:12")

    def test_fmtd_formats_datetime_value_with_types_format_str(self):
        dt = SimpleDatetime(tfmtdt=datetime(2021, 3, 3, 12, 12, 12))
        self.assertEqual(dt.tojson()['tfmtdt'],"2021年03月03日 12:12:12")
