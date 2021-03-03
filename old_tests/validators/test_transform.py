from unittest import TestCase
from typing import Dict, Any, Optional, TypedDict
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException


class TestTransformValidator(TestCase):

    def test_transform_validator_raises_if_param_is_not_callable(self):
        with self.assertRaisesRegex(ValueError, '5 is not a callable'):
            @jsonclass(class_graph='test_transform_1')
            class User(JSONObject):
                password: str = types.str.transform(5)

    def test_transform_validator_do_not_raise_if_param_is_not_callable(self):
        def t() -> str:
            return '5'
        @jsonclass(class_graph='test_transform_2')
        class User(JSONObject):
            password: str = types.str.transform(t)
