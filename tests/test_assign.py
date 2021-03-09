from __future__ import annotations
from unittest import TestCase
from tests.classes.linked_profile import LinkedProfile
from tests.classes.linked_user import LinkedUser
from tests.classes.linked_author import LinkedAuthor
from tests.classes.linked_article import LinkedArticle


class TestAssign(TestCase):

    def test_assign_sets_other_sides_single_link(self):
        user = LinkedUser(name='U')
        profile = LinkedProfile(name='P')
        user.profile = profile
        self.assertEqual(user.profile, profile)
        self.assertEqual(profile.user, user)
        user = LinkedUser(name='U')
        profile = LinkedProfile(name='P')
        profile.user = user
        self.assertEqual(user.profile, profile)
        self.assertEqual(profile.user, user)

    def test_assign_sets_other_sides_single_to_multiple_link(self):
        article1 = LinkedArticle(name='A1')
        article2 = LinkedArticle(name='A2')
        author = LinkedAuthor(name='Author', articles=[article1])
        article2.author = author
        self.assertEqual(article2.author, author)
        self.assertEqual(author.articles, [article1, article2])
