from __future__ import annotations
from unittest import TestCase
from tests.classes.linked_profile import LinkedProfile
from tests.classes.linked_user import LinkedUser
from tests.classes.linked_author import LinkedAuthor
from tests.classes.linked_article import LinkedArticle
from tests.classes.linked_customer import LinkedCustomer
from tests.classes.linked_product import LinkedProduct


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

    def test_assign_unsets_other_sides_single_link(self):
        user = LinkedUser(name='U')
        profile = LinkedProfile(name='P')
        user.profile = profile
        user.profile = None
        self.assertEqual(user.profile, None)
        self.assertEqual(profile.user, None)
        self.assertEqual(user._unlinked_objects['profile'], [profile])
        self.assertEqual(profile._unlinked_objects['user'], [user])
        user = LinkedUser(name='U')
        profile = LinkedProfile(name='P')
        user.profile = profile
        profile.user = None
        self.assertEqual(user.profile, None)
        self.assertEqual(profile.user, None)
        self.assertEqual(user._unlinked_objects['profile'], [profile])
        self.assertEqual(profile._unlinked_objects['user'], [user])

    def test_assign_resets_other_sides_single_link(self):
        user = LinkedUser(name='U')
        profile = LinkedProfile(name='P')
        user.profile = profile
        user.profile = None
        user.profile = profile
        self.assertEqual(user.profile, profile)
        self.assertEqual(profile.user, user)
        self.assertEqual(user._unlinked_objects['profile'], [])
        self.assertEqual(profile._unlinked_objects['user'], [])

    def test_assign_sets_other_sides_single_to_multiple_link(self):
        article1 = LinkedArticle(name='A1')
        article2 = LinkedArticle(name='A2')
        author = LinkedAuthor(name='Author', articles=[article1])
        article2.author = author
        self.assertEqual(article2.author, author)
        self.assertEqual(author.articles, [article1, article2])
        article1 = LinkedArticle(name='A1')
        article2 = LinkedArticle(name='A2')
        author = LinkedAuthor(name='Author')
        author.articles = [article1, article2]
        self.assertEqual(article1.author, author)
        self.assertEqual(article2.author, author)
        self.assertEqual(author.articles, [article1, article2])

    def test_assign_unsets_other_sides_single_to_multiple_link(self):
        article1 = LinkedArticle(name='A1')
        article2 = LinkedArticle(name='A2')
        author = LinkedAuthor(name='Author', articles=[article1])
        article2.author = author
        article2.author = None
        self.assertEqual(article2.author, None)
        self.assertEqual(author.articles, [article1])
        self.assertEqual(article2._unlinked_objects['author'], [author])
        self.assertEqual(author._unlinked_objects['articles'], [article2])
        article1 = LinkedArticle(name='A1')
        article2 = LinkedArticle(name='A2')
        author = LinkedAuthor(name='Author')
        author.articles = [article1, article2]
        author.articles = []
        self.assertEqual(article1.author, None)
        self.assertEqual(article2.author, None)
        self.assertEqual(author.articles, [])
        self.assertEqual(article1._unlinked_objects['author'], [author])
        self.assertEqual(article2._unlinked_objects['author'], [author])
        self.assertEqual(author._unlinked_objects['articles'],
                         [article1, article2])

    def test_assign_resets_other_sides_single_to_multiple_link(self):
        article1 = LinkedArticle(name='A1')
        article2 = LinkedArticle(name='A2')
        author = LinkedAuthor(name='Author', articles=[article1])
        article2.author = author
        article1.author = None
        article2.author = None
        author.articles = [article1, article2]
        self.assertEqual(article1.author, author)
        self.assertEqual(article2.author, author)
        self.assertEqual(author.articles, [article1, article2])
        self.assertEqual(article1._unlinked_objects['author'], [])
        self.assertEqual(article2._unlinked_objects['author'], [])
        self.assertEqual(author._unlinked_objects['articles'], [])

    def test_assign_sets_other_sides_multiple_to_multiple_link(self):
        c1 = LinkedCustomer(name='C1')
        c2 = LinkedCustomer(name='C2')
        p1 = LinkedProduct(name='P1')
        p2 = LinkedProduct(name='P2')
        p1.customers.extend([c1, c2])
        p2.customers.extend([c1, c2])
        self.assertEqual(c1.products, [p1, p2])
        self.assertEqual(c2.products, [p1, p2])
        self.assertEqual(p1.customers, [c1, c2])
        self.assertEqual(p2.customers, [c1, c2])

    def test_assign_unsets_other_sides_multiple_to_multiple_link(self):
        c1 = LinkedCustomer(name='C1')
        c2 = LinkedCustomer(name='C2')
        p1 = LinkedProduct(name='P1')
        p2 = LinkedProduct(name='P2')
        p1.customers.extend([c1, c2])
        p2.customers.extend([c1, c2])
        p1.customers = []
        p2.customers = []
        self.assertEqual(c1.products, [])
        self.assertEqual(c2.products, [])
        self.assertEqual(p1.customers, [])
        self.assertEqual(p2.customers, [])
        self.assertEqual(c1._unlinked_objects['products'], [p1, p2])
        self.assertEqual(c2._unlinked_objects['products'], [p1, p2])
        self.assertEqual(p1._unlinked_objects['customers'], [c1, c2])
        self.assertEqual(p2._unlinked_objects['customers'], [c1, c2])

    def test_assign_resets_other_sides_multiple_to_multiple_link(self):
        c1 = LinkedCustomer(name='C1')
        c2 = LinkedCustomer(name='C2')
        p1 = LinkedProduct(name='P1')
        p2 = LinkedProduct(name='P2')
        p1.customers.extend([c1, c2])
        p2.customers.extend([c1, c2])
        p1.customers = []
        p2.customers = []
        p1.customers.extend([c1, c2])
        p2.customers.extend([c1, c2])
        self.assertEqual(c1.products, [p1, p2])
        self.assertEqual(c2.products, [p1, p2])
        self.assertEqual(p1.customers, [c1, c2])
        self.assertEqual(p2.customers, [c1, c2])
        self.assertEqual(c1._unlinked_objects['products'], [])
        self.assertEqual(c2._unlinked_objects['products'], [])
        self.assertEqual(p1._unlinked_objects['customers'], [])
        self.assertEqual(p2._unlinked_objects['customers'], [])
