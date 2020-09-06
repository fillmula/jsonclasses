import unittest
from jsonclasses import jsonclass, PersistableJSONObject
from datetime import datetime

class TestPersistableJSONObject(unittest.TestCase):

  def test_persistable_json_object_has_created_at_on_initializing(self):
    o = PersistableJSONObject()
    self.assertTrue(type(o.created_at) is datetime)
    self.assertTrue(o.created_at < datetime.now())

  def test_persistable_json_object_has_updated_at_on_initializing(self):
    o = PersistableJSONObject()
    self.assertTrue(type(o.updated_at) is datetime)
    self.assertTrue(o.updated_at < datetime.now())

  def test_persistable_json_object_has_id_with_default_value_none(self):
    o = PersistableJSONObject()
    self.assertTrue(o.id is None)
