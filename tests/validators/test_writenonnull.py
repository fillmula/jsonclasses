import unittest
from jsonclasses import jsonclass, JSONObject, types


class TestWritenonnullValidator(unittest.TestCase):

    def test_writenonnull_fields_can_accept_initial_value(self):
        @jsonclass(class_graph='test_writenonnull_1')
        class User(JSONObject):
            nickname: str = types.str.writenonnull.required
        user = User(nickname='John')
        self.assertEqual(user.nickname, 'John')

    def test_writenonnull_fields_can_accept_default_value(self):
        @jsonclass(class_graph='test_writenonnull_2')
        class User(JSONObject):
            nickname: str = types.str.writenonnull.default('Peter').required
        user = User()
        self.assertEqual(user.nickname, 'Peter')

    def test_writenonnull_fields_can_accept_nonnull_value(self):
        @jsonclass(class_graph='test_writenonnull_3')
        class User(JSONObject):
            nickname: str = types.str.writenonnull.required
        user = User(nickname='John')
        user.set(nickname='Peter')
        self.assertEqual(user.nickname, 'Peter')

    def test_writenonnull_fields_cannot_accept_null_value(self):
        @jsonclass(class_graph='test_writenonnull_4')
        class User(JSONObject):
            nickname: str = types.str.writenonnull.required
        user = User(nickname='John')
        user.set(nickname=None)
        self.assertEqual(user.nickname, 'John')
