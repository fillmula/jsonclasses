import unittest
from jsonclasses import jsonclass, JSONObject
from datetime import datetime, date

class TestJSONObjectSet(unittest.TestCase):

  def test_set_without_arguments_wont_change_anything(self):
    @jsonclass(graph='test_set_1')
    class Contact(JSONObject):
      name: str
      address: str
    contact = Contact(name='John', address='Balk')
    contact.set()
    self.assertEqual(contact.__dict__, { 'name': 'John', 'address': 'Balk' })

  def test_set_with_keyed_arguments_updates_value(self):
    @jsonclass(graph='test_set_2')
    class BusinessCard(JSONObject):
      name: str
      phone_no: str
    card = BusinessCard(name='John', phone_no='012345678')
    card.set(phone_no='22')
    self.assertEqual(card.__dict__, { 'name': 'John', 'phone_no': '22' })

  def test_set_with_dict_argument_updates_value(self):
    @jsonclass(graph='test_set_3')
    class BusinessCard(JSONObject):
      name: str
      phone_no: str
    card = BusinessCard(name='John', phone_no='012345678')
    card.set(**{ 'phone_no': '234' })
    self.assertEqual(card.__dict__, { 'name': 'John', 'phone_no': '234' })

  def test_set_is_chainable(self):
    @jsonclass(graph='test_set_4')
    class Rainbow(JSONObject):
      red: int
      orange: int
      yellow: int
      green: int
      indigo: int
      blue: int
      purple: int
    rainbow = Rainbow(red=1).set(orange=2).set(yellow=3).set(green=4).set(indigo=5)
    self.assertEqual(
      rainbow.__dict__,
      { 'red': 1, 'orange': 2, 'yellow': 3, 'green': 4, 'indigo': 5, 'blue': None, 'purple': None }
    )

  def test_set_handles_date_transform(self):
    @jsonclass(graph='test_set_5')
    class Semester(JSONObject):
      start: date
      end: date
    semester = Semester()
    semester.set(**{ 'start': '2020-02-20', 'end': '2020-06-30' })
    self.assertEqual(
      semester.__dict__,
      {
        'start': date.fromisoformat('2020-02-20'),
        'end': date.fromisoformat('2020-06-30')
      }
    )

  def test_set_handles_datetime_transform(self):
    @jsonclass(graph='test_set_6')
    class Timer(JSONObject):
      expired_at: datetime
    timer = Timer()
    timer.set(**{ 'expiredAt': '2020-08-29T06:38:34.242Z' })
    self.assertEqual(
      timer.__dict__,
      {
        'expired_at': datetime.fromisoformat('2020-08-29T06:38:34.242000')
      }
    )

  def test_set_ignores_redundant_keys(self):
    @jsonclass(graph='test_set_7')
    class Size(JSONObject):
      width: float
      height: float
    size = Size()
    size.set(width=10.5, height=7.5, depth=2.5)
    self.assertEqual(size.__dict__, { 'width': 10.5, 'height': 7.5 })

  def test_set_none_on_fields_from_dict(self):
    @jsonclass(graph='test_set_8')
    class Size(JSONObject):
      width: float
      height: float
    size = Size(width=2, height=5)
    size.set(**{ 'width': None })
    self.assertEqual(size.__dict__, { 'width': None, 'height': 5 })

  def test_set_none_on_fields_from_keyed_arguments(self):
    @jsonclass(graph='test_set_9')
    class Size(JSONObject):
      width: float
      height: float
    size = Size(width=2, height=5)
    size.set(width=None)
    self.assertEqual(size.__dict__, { 'width': None, 'height': 5 })

  def test_set_auto_convert_camelcase_keys_into_snakecase(self):
    @jsonclass(graph='test_set_10')
    class Coupon(JSONObject):
      minimum_purchase_value: int
      discount_rate: float
    coupon = Coupon()
    coupon.set(**{ 'minimumPurchaseValue': 1000, 'discountRate': 0.5 })
    self.assertEqual(coupon.minimum_purchase_value, 1000)
    self.assertEqual(coupon.discount_rate, 0.5)

  def test_set_will_not_modify_date_if_date_is_passed_in(self):
    @jsonclass(graph='test_set_11')
    class Semester(JSONObject):
      start: date
      end: date
    start = date.fromisoformat('2020-10-10')
    end = date.fromisoformat('2020-12-12')
    semester = Semester()
    semester.set(start=start, end=end)
    self.assertEqual(semester.start, start)
    self.assertEqual(semester.end, end)

  def test_set_will_not_modify_datetime_if_datetime_is_passed_in(self):
    @jsonclass(graph='test_set_12')
    class Timer(JSONObject):
      expired_at: datetime
    expired_at = datetime.fromisoformat('2020-10-10T05:03:02.999888')
    timer = Timer()
    timer.set(**{ 'expiredAt': expired_at })
    self.assertEqual(timer.expired_at, expired_at)
