import unittest
from typing import Dict, Any, Optional, TypedDict
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException


class TestShapeValidator(unittest.TestCase):

    def test_shape_validator_validates_subfields(self):
        @jsonclass(class_graph='test_shape_1')
        class User(JSONObject):
            address: dict = types.nonnull.shape({
                'line1': types.str.required,
                'line2': types.str
            })
        user = User()
        self.assertRaisesRegex(ValidationException, '\'address\\.line1\' should not be None', user.validate)

    def test_shape_validator_do_not_throw_if_subfields_are_ok(self):
        @jsonclass(class_graph='test_shape_2')
        class User(JSONObject):
            address: dict = types.nonnull.shape({
                'line1': types.str.required,
                'line2': types.str
            }).required
        user = User(address={'line1': 'Shanghai'})
        user.validate()

    def test_shape_validator_assigns_none_for_accessing(self):
        @jsonclass(class_graph='test_shape_3')
        class User(JSONObject):
            address: dict = types.shape({
                'line1': types.str,
                'line2': types.str,
                'line3': types.str
            }).required
        user = User(address={'line1': 'Sydney'})
        self.assertEqual(user.__fdict__, {
            'address': {'line1': 'Sydney', 'line2': None, 'line3': None}
        })

    def test_shape_validator_sanitizes_input(self):
        @jsonclass(class_graph='test_shape_4')
        class User(JSONObject):
            address: dict = types.shape({
                'line1': types.str,
                'line2': types.str,
                'line3': types.str
            }).required
        user = User(address={'line1': 'Sydney', 'haha': 'I\'m here'})
        self.assertEqual(user.__fdict__, {
            'address': {'line1': 'Sydney', 'line2': None, 'line3': None}
        })

    def test_shape_should_camelize_keys_when_serializing_if_its_the_class_setting(self):
        @jsonclass(class_graph='test_shape_5', camelize_json_keys=True)
        class Score(JSONObject):
            scores: dict = types.shape({
                'student_a': types.int,
                'student_b': types.int
            })
        score = Score(scores={'student_a': 2, 'student_b': 4})
        self.assertEqual(score.tojson(), {'scores': {'studentA': 2, 'studentB': 4}})

    def test_shape_should_not_camelize_keys_when_serializing_if_its_the_class_setting(self):
        @jsonclass(class_graph='test_shape_6', camelize_json_keys=False)
        class Score(JSONObject):
            scores: dict = types.shape({
                'student_a': types.int,
                'student_b': types.int
            })
        score = Score(scores={'student_a': 2, 'student_b': 4})
        self.assertEqual(score.tojson(), {'scores': {'student_a': 2, 'student_b': 4}})

    def test_shape_should_handle_camelized_keys_when_initializing_if_its_the_class_setting(self):
        @jsonclass(class_graph='test_shape_7', camelize_json_keys=True)
        class Score(JSONObject):
            scores: dict = types.shape({
                'student_a': types.int,
                'student_b': types.int
            })
        score = Score(scores={'studentA': 2, 'studentB': 4})
        self.assertEqual(score.__fdict__, {'scores': {'student_a': 2, 'student_b': 4}})

    def test_shape_should_not_handle_camelized_keys_when_initializing_if_its_the_class_setting(self):
        @jsonclass(class_graph='test_shape_8', camelize_json_keys=False)
        class Score(JSONObject):
            scores: dict = types.shape({
                'student_a': types.int,
                'student_b': types.int
            })
        score = Score(scores={'student_a': 2, 'student_b': 4})
        self.assertEqual(score.__fdict__, {'scores': {'student_a': 2, 'student_b': 4}})

    def test_shape_produce_error_messages_for_all_items(self):
        @jsonclass(class_graph='test_shape_9')
        class Quiz(JSONObject):
            numbers: Dict[str, int] = types.shape({
                'a': types.int.min(140),
                'b': types.int.min(150)
            })
        quiz = Quiz(numbers={'a': 1, 'b': 2, })
        self.assertRaisesRegex(ValidationException, 'numbers\\.b', quiz.validate)

    def test_strict_shape_raises_if_key_is_not_allowed(self):
        @jsonclass(class_graph='test_shape_10')
        class Setting(JSONObject):
            info: Dict[str, Any] = types.strict.shape({
                'ios': types.bool.required,
                'android': types.bool.required
            })
        with self.assertRaisesRegex(ValidationException, "Unallowed key 'email' at 'info'\\."):
            Setting(info={'ios': True, 'android': False, 'email': True})

    def test_strict_shape_doesnt_raise_if_keys_are_ok(self):
        @jsonclass(class_graph='test_shape_11')
        class Setting(JSONObject):
            info: Dict[str, Any] = types.strict.shape({
                'ios': types.bool.required,
                'android': types.bool.required
            })
        Setting(info={'ios': True, 'android': False})

    def test_shape_accepts_shorthand_types(self):
        @jsonclass(class_graph='test_shape_12')
        class User(JSONObject):
            address: dict = types.nonnull.shape({
                'line1': str,
                'line2': int
            })
        user = User()
        self.assertRaisesRegex(ValidationException, '\'address\\.line1\' should not be None', user.validate)

    def test_shape_accepts_optional_shorthand_types(self):
        @jsonclass(class_graph='test_shape_13')
        class User(JSONObject):
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
        class User(JSONObject):
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
        class User(JSONObject):
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
        class User(JSONObject):
            settings: Settings

        user = User(settings={'ios': True})
        self.assertRaisesRegex(ValidationException,
                               "'settings\\.name' should not be None",
                               user.validate)
