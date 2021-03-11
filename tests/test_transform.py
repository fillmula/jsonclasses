from __future__ import annotations
from unittest import TestCase
from jsonclasses import jsonclass, types


class TestTransform(TestCase):

    def test_transform_raises_if_param_is_not_callable(self):
        with self.assertRaisesRegex(ValueError, 'transformer is not callable'):
            @jsonclass
            class WrongTransform:
                name: str = types.str.transform(5).required

    def test_transformer(self):
        pass
