from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.super_oneof import SuperOneOf


class TestOneOf(TestCase):

    def test_oneof_wont_raise_with_constant(self):
        SuperOneOf(valconst='abc').validate()

    def test_oneof_raises_with_constant(self):
        self.assertRaises(ValidationException, SuperOneOf(valconst='qwe').validate)

    def test_oneof_wont_raise_with_callable(self):
        SuperOneOf(valcallable='abc').validate()

    def test_oneof_raises_with_callable(self):
        self.assertRaises(ValidationException, SuperOneOf(valcallable='qwe').validate)

    def test_oneof_wont_raise_with_types(self):
        SuperOneOf(valtypes='abc').validate()

    def test_oneof_raises_with_types(self):
        self.assertRaises(ValidationException, SuperOneOf(valtypes='qwe').validate)
