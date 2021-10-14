from __future__ import annotations
from random import random
from tests.classes.super_random import SuperRandom
from unittest import TestCase

class TestRandomFloat(TestCase):

    def test_random_float_generate_a_random_float_value(self):
        i = SuperRandom(random_float=10.0)
        self.assertEqual(i.random_float, 10.0)
