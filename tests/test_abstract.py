from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import AbstractJSONClassException
from tests.classes.abstract_object import (AbstractObject, MyObject,
                                           NonAbstractObject,
                                           DefaultNonAbstractObject)


class TestAbstractClass(TestCase):

    def test_abstract_class_cannot_be_initialized(self):
        with self.assertRaises(AbstractJSONClassException) as context:
            AbstractObject()
        self.assertEqual(
            context.exception.message,
            'AbstractObject is an abstract class and should not be '
            'initialized')

    def test_non_abstract_class_can_be_initialized(self):
        NonAbstractObject()

    def test_abstract_classs_non_abstract_subclass_can_be_initialized(self):
        MyObject()

    def test_abstract_class_class_is_not_abstract_by_default(self):
        DefaultNonAbstractObject()
