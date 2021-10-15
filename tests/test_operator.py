from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.operator import (AsopUser, AsopTeam, AsopdUser, AsopdTeam)


class TestOperator(TestCase):

    def test_asop_assigns_transformed_to_field_if_operator_is_present(self):
        user = AsopUser(name='U')
        team = AsopTeam(name='T')
        team.opby(user)
        self.assertEqual(team.owner, user)
        team.validate()

    def test_asop_is_invalid_when_operator_is_not_present_on_create(self):
        team = AsopTeam(name='T')
        with self.assertRaises(ValidationException) as context:
            team.validate()
        self.assertEqual(context.exception.keypath_messages['owner'],
                         "no operator being assigned")

    def test_asop_is_not_invalid_when_updating_other_fields(self):
        team = AsopTeam(name='T')
        setattr(team, '_is_new', False)
        team.validate()

    def test_asop_is_invalid_when_operator_is_not_present_on_update(self):
        team = AsopTeam(name='T')
        setattr(team, '_is_new', False)
        setattr(team, '_modified_fields', ('owner',))
        with self.assertRaises(ValidationException) as context:
            team.validate()
        self.assertEqual(context.exception.keypath_messages['owner'],
                         "no operator being assigned")

    def test_asopd_assigns_directly_to_field_if_operator_is_present(self):
        user = AsopdUser(name='U')
        team = AsopdTeam(name='T')
        team.opby(user)
        self.assertEqual(team.owner, user)
        team.validate()

    def test_asopd_is_invalid_when_operator_is_not_present_on_create(self):
        team = AsopdTeam(name='T')
        with self.assertRaises(ValidationException) as context:
            team.validate()
        self.assertEqual(context.exception.keypath_messages['owner'],
                         "no operator being assigned")

    def test_asopd_is_not_invalid_when_updating_other_fields(self):
        team = AsopdTeam(name='T')
        setattr(team, '_is_new', False)
        team.validate()

    def test_asopd_is_invalid_when_operator_is_not_present_on_update(self):
        team = AsopdTeam(name='T')
        setattr(team, '_is_new', False)
        setattr(team, '_modified_fields', ('owner',))
        with self.assertRaises(ValidationException) as context:
            team.validate()
        self.assertEqual(context.exception.keypath_messages['owner'],
                         "no operator being assigned")
