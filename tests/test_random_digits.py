from __future__ import annotations
from random import random
from tests.classes.super_random import SuperRandom
from unittest import TestCase

class TestRandomDigits(TestCase):

    def test_random_digits_generates_random_digits_as_result(self):
        i = SuperRandom(random_digits=1)
        self.assertEqual(type(i.random_digits), type('1'))

    def test_random_digits_generates_random_callable_as_result(self):
        i = SuperRandom(c_random_digits=1)
        self.assertEqual(type(i.c_random_digits), type('1'))

    def test_random_digits_generates_random_types_as_result(self):
        i = SuperRandom(t_random_digits=1)
        self.assertEqual(type(i.t_random_digits), type('1'))
