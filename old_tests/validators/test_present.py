from __future__ import annotations
from unittest import TestCase
from jsonclasses import jsonclass, JSONObject, types, ValidationException


@jsonclass(class_graph='test_present_1')
class Group(JSONObject):
    id: int = types.int.primary
    name: str
    template: Template = types.instanceof('Template').linkedby('group').present


@jsonclass(class_graph='test_present_1')
class Template(JSONObject):
    id: int = types.int.primary
    name: str
    group: Group = types.linkto.instanceof('Group').required


class TestPresentValidator(TestCase):

    def test_present_raises_on_blank_foreign_keys(self):
        group = Group(name='group')
        self.assertRaisesRegex(ValidationException,
                               "Value at 'template' should be present\\.",
                               group.validate)

    def test_present_doesnt_raise_on_present_foreign_field(self):
        group = Group(name='group', id=1)
        group.template = Template(name='template', id=1)
        self.assertEqual(group.template.group, group)
        group.validate()
