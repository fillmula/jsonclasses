import unittest
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException


class TestTrimValidator(unittest.TestCase):

    def test_trim_validator_trims_string(self):
        @jsonclass(class_graph='test_trim_1')
        class BadData(JSONObject):
            bad_value: str = types.str.trim
        bad_data = BadData(bad_value='  I am bad.  ')
        self.assertEqual(bad_data.bad_value, 'I am bad.')
