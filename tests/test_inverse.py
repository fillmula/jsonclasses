from __future__ import annotations
from unittest import TestCase
from tests.classes.super_inverse import SuperInverse


class TestInverse(TestCase):

    def test_inverse_transforms_false_if_bool_is_true(self):
        b = SuperInverse(iv=False)
        self.assertEqual(b.iv, True)

    def test_inverse_transforms_true_if_bool_is_false(self):
        b = SuperInverse(iv=True)
        self.assertEqual(b.iv, False)
