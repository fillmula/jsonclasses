import unittest
from typing import Dict, Any, Optional, TypedDict
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException


class TestShapeValidator(unittest.TestCase):

    def test_shape_accepts_shorthand_types(self):
        @jsonclass(class_graph='test_shape_12')
        class User:
            address: dict = types.nonnull.shape({
                'line1': str,
                'line2': int
            })
        user = User()
        self.assertRaisesRegex(ValidationException, '\'address\\.line1\' should not be None', user.validate)

    def test_shape_accepts_optional_shorthand_types(self):
        @jsonclass(class_graph='test_shape_13')
        class User:
            address: dict = types.nonnull.shape({
                'line1': Optional[str],
                'line2': Optional[int]
            })
        User().validate()

    def test_shape_can_be_marked_with_typed_dict(self):

        class Settings(TypedDict):
            ios: bool
            android: bool
            name: str

        @jsonclass(class_graph='test_shape_14')
        class User:
            settings: Settings = types.nonnull.shape({
                'ios': types.bool.default(True).required,
                'android': types.bool.default(True).required,
                'name': types.str.required
            })
        user = User()
        self.assertRaisesRegex(ValidationException, "settings\\.name' should not be None", user.validate)

    def test_shape_can_accept_default_values(self):

        class Settings(TypedDict):
            ios: bool
            android: bool
            name: str

        @jsonclass(class_graph='test_shape_15')
        class User:
            settings: Settings = types.nonnull.shape({
                'ios': types.bool.default(True).required,
                'android': types.bool.default(True).required,
                'name': types.str.default('unnamed').required
            })
        user = User(settings={'android': False})
        self.assertEqual(user.settings['ios'], True)
        self.assertEqual(user.settings['android'], False)
        self.assertEqual(user.settings['name'], 'unnamed')

    def test_shape_generates_validator_from_typed_dict_type(self):
        class Settings(TypedDict):
            ios: bool
            android: Optional[bool]
            name: str

        @jsonclass(class_graph='test_shape_16')
        class User:
            settings: Settings

        user = User(settings={'ios': True})
        self.assertRaisesRegex(ValidationException,
                               "'settings\\.name' should not be None",
                               user.validate)
