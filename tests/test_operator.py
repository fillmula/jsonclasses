from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.operator import OpUser, OpTeam


class TestOperator(TestCase):

    def test_user_can_pass_validation_if_is_owner(self):
        user = OpUser(name='U')
        team = OpTeam(name='T')
        team.owner = user
        team.opby(user)
        team.validate()

    def test_user_cannot_pass_validation_if_is_not_owner(self):
        user = OpUser(name='U')
        user2 = OpUser(name='Z')
        team = OpTeam(name='T')
        team.owner = user2
        team.opby(user)
        with self.assertRaises(ValidationException) as context:
            team.validate()
        self.assertEqual(context.exception.keypath_messages['name'],
                         "unauthorized operation")
