from __future__ import annotations
from datetime import date, datetime
from tests.classes.simple_datetime import SimpleDatetime
from unittest import TestCase

class TestFormatDatetime(TestCase):

    def test_fmtd_formats_datetime_value(self):
        time = datetime.now()
        dt = SimpleDatetime(fmtdt=time)
        self.assertEqual(dt.tojson()['fmtdt'], time.strftime("%Y年%m月%d日 %H:%M:%S"))

    def test_fmtd_formats_date_value(self):
        time = date.today()
        d = SimpleDatetime(fmtd=time)
        self.assertEqual(d.tojson()['fmtd'], time.strftime("%Y年%m月%d日"))

    def test_fmtd_formats_datetime_str_value(self):
        dts = SimpleDatetime(fmtdts="2021-11-20T03:03:03.333Z")
        self.assertEqual(dts.tojson()['fmtdts'], "2021年11月20日 03:03:03")

    def test_fmtd_formats_date_str_value(self):
        ds = SimpleDatetime(fmtds="2021-11-20")
        self.assertEqual(ds.tojson()['fmtds'], "2021年11月20日")
