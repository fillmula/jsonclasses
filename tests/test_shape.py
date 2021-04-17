from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_config_user import SimpleConfigUser
from tests.classes.simple_folder import SimpleFolder
from tests.classes.simple_node import SimpleNode
from tests.classes.simple_shape_setting import SimpleShapeSetting
from tests.classes.simple_shorthand_setting import SimpleShorthandSetting
from tests.classes.default_shape_value import DefaultShapeValue


class TestShape(TestCase):

    def test_shape_accepts_shorthand_types(self):
        setting = SimpleShapeSetting()
        setting.email['auto_send'] = '5'
        setting.email['receive_promotion'] = '5'
        self.assertRaisesRegex(ValidationException,
                               "Value '5' at 'email.auto_send' should be "
                               "bool.",
                               setting.validate)

    def test_shape_accepts_optional_shorthand_types(self):
        setting = SimpleShorthandSetting()
        setting.email['auto_send'] = '5'
        setting.email['receive_promotion'] = '5'
        self.assertRaisesRegex(ValidationException,
                               "Value '5' at 'email.auto_send' should be "
                               "bool.",
                               setting.validate)
        setting = SimpleShorthandSetting()
        setting.validate()

    def test_shape_accepts_typed_dict_type(self):
        value = DefaultShapeValue(
            settings={'ios': '2', 'android': '2', 'name': '4'})
        self.assertRaisesRegex(
            ValidationException,
            "Value '2' at 'settings.ios' should be bool.",
            value.validate)

    def test_shape_validates_inner_fields(self):
        user = SimpleConfigUser(config={})
        self.assertRaisesRegex(ValidationException,
                               '\'config\\.ios\' should not be None',
                               user.validate)

    def test_shape_doesnt_raise_on_validation_if_inner_fields_are_ok(self):
        user = SimpleConfigUser(config={'ios': True, 'android': True})
        user.validate()

    def test_shape_assigns_none_on_inner_fields_for_accessing(self):
        user = SimpleConfigUser(config={})
        self.assertEqual(user.config, {'ios': None, 'android': None})

    # TODO: make shape work according to strict settings
    def test_shape_sanitizes_input(self):
        user = SimpleConfigUser(config={'haha': True, 'android': False})
        self.assertEqual(user.config, {'ios': None, 'android': False})

    def test_shape_underscores_keys_on_init(self):
        folder = SimpleFolder(
            config={'displaySize': True, 'displayDate': False})
        self.assertEqual(folder.config,
                         {'display_size': True, 'display_date': False})

    def test_shape_doesnt_underscore_keys_on_init_if_specified(self):
        node = SimpleNode(
            config={'displaySize': True, 'display_Date': False})
        self.assertEqual(node.config,
                         {'display_size': None, 'display_date': None})

    def test_shape_camelizes_keys_on_tojson(self):
        folder = SimpleFolder(
            config={'displaySize': True, 'displayDate': False})
        self.assertEqual(folder.tojson()['config'],
                         {'displaySize': True, 'displayDate': False})

    def test_shape_doesnt_camelize_keys_on_tojson(self):
        node = SimpleNode(
            config={'display_size': True, 'display_date': False})
        self.assertEqual(node.tojson()['config'],
                         {'display_size': True, 'display_date': False})

    def test_shape_produce_validation_error_message_for_one_item(self):
        node = SimpleNode(config={})
        with self.assertRaises(ValidationException) as context:
            node.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['config.display_size'],
                         "Value at 'config.display_size' should not be None.")

    def test_strict_shape_raises_if_key_is_not_allowed(self):
        with self.assertRaisesRegex(ValidationException,
                                    "Unallowed key 'a' at 'config'\\."):
            SimpleFolder(config={'a': True, 'b': False})
