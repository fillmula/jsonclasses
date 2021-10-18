from __future__ import annotations
from random import random
from tests.classes.super_random import SuperRandom
from unittest import TestCase

class TestRandomInt(TestCase):

    def test_random_int_generate_a_random_int_value(self):
        i = SuperRandom(random_int=10)
        self.assertEqual(i.random_int, 10)

    def test_random_int_generate_a_random_callable_value(self):
        i = SuperRandom(c_random_int=10)
        self.assertEqual(i.c_random_int, 10)

    def test_random_int_generate_a_random_types_value(self):
        i = SuperRandom(t_random_int=10)
        self.assertEqual(i.t_random_int, 10)
