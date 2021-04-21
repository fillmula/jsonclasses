from __future__ import annotations
from unittest import TestCase
from tests.classes.transform_name import TransformName, CTransformName


class TestTransform(TestCase):

    def test_transform_wont_handle_none(self):
        name = TransformName(name=None)
        self.assertEqual(name.name, None)

    def test_transform_transforms_with_1_param(self):
        name = TransformName(name='Thuan I')
        self.assertEqual(name.name, 'Thuan Iq')

    def test_transform_transforms_takes_optional_context(self):
        name = CTransformName(name='Ua Ai Kai Nang')
        self.assertEqual(name.name, 'Ua Ai Kai NangUa Ai Kai Nang')
