import unittest
from jsonclasses.json_object import JSONObject

class TestJSONObject(unittest.TestCase):

    def test_initialize_with_dict_fill_none_on_blank_keys(self):
      class TestPoint(JSONObject):
        x: int
        y: int
      input = { 'x': 50 }
      point = TestPoint(**input)
      self.assertEqual(point, { 'x': 50, 'y': None })

if __name__ == '__main__':
    unittest.main()
