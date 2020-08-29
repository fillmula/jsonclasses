import unittest
from jsonclasses import jsonclass, JSONObject
from datetime import datetime, date

class TestJSONObjectSerialize(unittest.TestCase):

  def test_serialize_str_to_str(self):
    @jsonclass
    class Contact(JSONObject):
      name: str
      address: str
    contact = Contact(name="John", address="Flamingo Road")
    self.assertEqual(contact.to_json(), { 'name': 'John', 'address': 'Flamingo Road' })

  def test_serialize_int_to_int(self):
    @jsonclass
    class Point(JSONObject):
      x: int
      y: int
    point = Point(x=5, y=6)
    self.assertEqual(point.to_json(), { 'x': 5, 'y': 6 })

  def test_serialize_float_to_float(self):
    @jsonclass
    class Point(JSONObject):
      x: float
      y: float
    point = Point(x=5.5, y=6.6)
    self.assertEqual(point.to_json(), { 'x': 5.5, 'y': 6.6 })

  def test_serialize_bool_to_bool(self):
    @jsonclass
    class Status(JSONObject):
      active: bool
      enabled: bool
    status = Status(active=True, enabled=False)
    self.assertEqual(status.to_json(), { 'active': True, 'enabled': False })

  def test_serialize_datetime_to_iso_str(self):
    @jsonclass
    class Timer(JSONObject):
      expired_at: datetime
    timer = Timer(**{ 'expiredAt': '2020-08-29T06:38:34.242000' })
    self.assertEqual(timer.to_json(), { 'expiredAt': '2020-08-29T06:38:34.242Z' })

  def test_serialize_date_to_iso_str(self):
    @jsonclass
    class Countdown(JSONObject):
      day: date
    countdown = Countdown(**{ 'day': '2020-08-29' })
    self.assertEqual(countdown.to_json(), { 'day': '2020-08-29T00:00:00.000Z' })
