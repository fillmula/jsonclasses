from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.group_template import Group, Template


class TestPresent(TestCase):

    def test_present_raises_on_blank_foreign_keys(self):
        group = Group(name='group')
        self.assertRaisesRegex(ValidationException,
                               "value is not present",
                               group.validate)

    def test_present_doesnt_raise_on_present_foreign_field(self):
        group = Group(name='group', id=1)
        group.template = Template(name='template', id=1)
        self.assertEqual(group.template.group, group)
        group.validate()
