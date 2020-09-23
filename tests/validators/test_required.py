import unittest
from jsonclasses import jsonclass, JSONObject, types, ValidationException


class TestRequiredValidator(unittest.TestCase):

    def test_required_raises_on_embedded_none(self):
        @jsonclass(graph='test_required_1')
        class ClassOne(JSONObject):
            a: str = types.str.required
        item = ClassOne()
        self.assertRaisesRegex(
            ValidationException,
            "Value at 'a' should not be None\\.",
            item.validate)

    def test_required_raises_on_none_local_key(self):
        @jsonclass(graph='test_required_2')
        class ClassOne(JSONObject):
            a: str = types.str.required

        @jsonclass(graph='test_required_2')
        class ClassTwo(JSONObject):
            o: ClassOne = types.linkto.instanceof(ClassOne).required
        item = ClassTwo()
        self.assertRaisesRegex(
            ValidationException,
            "Value at 'o' should not be None\\.",
            item.validate)

    def test_required_does_not_raise_on_presence_local_key(self):
        @jsonclass(graph='test_required_3')
        class ClassOne(JSONObject):
            a: str = types.str.required

        @jsonclass(graph='test_required_3')
        class ClassTwo(JSONObject):
            o: ClassOne = types.linkto.instanceof(ClassOne).required
        item = ClassTwo()
        setattr(item, 'o_id', 5)
        item.validate()

    def test_required_does_not_raise_on_value_present(self):
        @jsonclass(graph='test_required_4')
        class ClassOne(JSONObject):
            a: str = types.str.required

        @jsonclass(graph='test_required_4')
        class ClassTwo(JSONObject):
            o: ClassOne = types.linkto.instanceof(ClassOne).required
        item = ClassTwo(o=ClassOne(a="b"))
        item.validate()
