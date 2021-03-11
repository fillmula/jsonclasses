from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_article import SimpleArticle
from tests.classes.linked_profile import LinkedProfile
from tests.classes.linked_user import LinkedUser


class TestRequired(TestCase):

    def test_required_raises_when_embedded_value_is_none(self):
        article = SimpleArticle()
        self.assertRaisesRegex(
            ValidationException,
            "Value at 'title' should not be None\\.",
            article.validate)

    def test_required_raises_when_local_key_is_none(self):
        profile = LinkedProfile(name='profile')
        self.assertRaisesRegex(
            ValidationException,
            "Value at 'user' should not be None\\.",
            profile.validate)

    def test_required_does_not_raise_when_local_key_is_present(self):
        profile = LinkedProfile(name='profile')
        setattr(profile, 'user_id', 5)
        profile.validate()

    def test_required_does_not_raise_when_local_key_value_is_present(self):
        profile = LinkedProfile(name='profile', user=LinkedUser(name='ok'))
        profile.validate()
