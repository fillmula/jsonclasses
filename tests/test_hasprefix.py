from __future__ import annotations
from tests.classes.super_affix import SuperAffix
from jsonclasses.excs import ValidationException
from unittest import TestCase


class TestHasPrefix(TestCase):

    def test_hasprefix_validates_a_str_is_prefix_of_original_str(self):
        hp = SuperAffix(hp='un')
        hp.validate()
