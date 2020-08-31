# import unittest
# from jsonclasses import jsonclass, JSONObject, types
# from datetime import datetime, date

# class TestJSONObjectValidate(unittest.TestCase):

#   def test_validate_throws_if_object_is_not_valid(self):
#     @jsonclass
#     class Contact(JSONObject):
#       name: str = types.str.required
#       address: str = types.str.required
#     contact = Contact()
#     contact.validate()
