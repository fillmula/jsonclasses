from __future__ import annotations
from unittest import TestCase
from tests.classes.local_key_author import LKAuthor, LKArticle
from tests.classes.linked_author import LinkedAuthor
from tests.classes.linked_article import LinkedArticle


class TestLocalKey(TestCase):

    def test_local_key_can_be_accessed(self):
        article = LKArticle(name='A')
        self.assertEqual(article.author_id, None)

    def test_set_object_modifies_local_key(self):
        author = LKAuthor(name='A')
        article = LKArticle(name='A', author=author)
        self.assertEqual(article.author_id, author.id)

    def test_set_local_key_resets_object(self):
        author = LKAuthor(name='A')
        article = LKArticle(name='A', author=author)
        self.assertEqual(article.author, author)
        self.assertEqual(author.articles[0], article)
        article.author_id = 500
        self.assertEqual(article.author, None)
        self.assertEqual(author.articles, [])

    def test_local_key_is_set_to_none_then_object_is_set_to_none(self):
        author = LKAuthor(name='A')
        article = LKArticle(name='A', author=author)
        self.assertEqual(article.author, author)
        self.assertEqual(author.articles[0], article)
        article.author_id = None
        self.assertEqual(article.author, None)
        self.assertEqual(author.articles, [])

    def test_object_is_set_to_none_then_local_key_is_set_to_none(self):
        author = LKAuthor(name='A')
        article = LKArticle(name='A', author=author)
        self.assertEqual(article.author, author)
        self.assertEqual(author.articles[0], article)
        article.author = None
        self.assertEqual(article.author_id, None)
        self.assertEqual(author.articles, [])

    def test_object_is_set_to_none_o_then_local_key_is_set_to_none(self):
        author = LKAuthor(name='A')
        article = LKArticle(name='A', author=author)
        self.assertEqual(article.author, author)
        self.assertEqual(author.articles[0], article)
        author.articles = []
        self.assertEqual(article.author_id, None)
        self.assertEqual(author.articles, [])

    def test_local_key_is_considered_modified_field(self):
        author = LKAuthor(name='A')
        article = LKArticle(name='A', author=author)
        setattr(author, '_is_new', False)
        setattr(article, '_is_new', False)
        article.author = None
        self.assertEqual(article.modified_fields, ('author',))
        self.assertEqual(author.modified_fields, ('articles',))

    def test_local_key_is_considered_modified_field_with_id_none_assign(self):
        author = LKAuthor(name='A')
        article = LKArticle(name='A', author=author)
        setattr(author, '_is_new', False)
        setattr(article, '_is_new', False)
        article.author_id = None
        self.assertEqual(article.modified_fields, ('author',))
        self.assertEqual(author.modified_fields, ('articles',))

    def test_local_key_is_considered_modified_field_with_id_assign(self):
        article = LKArticle(name='A', author=None)
        author = LKAuthor(name='A')
        setattr(author, '_is_new', False)
        setattr(article, '_is_new', False)
        article.author_id = author.id
        self.assertEqual(article.modified_fields, ('author',))

    def test_local_key_is_considered_modified_field_even_id_is_none(self):
        article = LinkedArticle(name='A', author=None)
        author = LinkedAuthor(name='A')
        setattr(author, '_is_new', False)
        setattr(article, '_is_new', False)
        article.author = author
        self.assertEqual(article.author_id, None)
        self.assertEqual(article.modified_fields, ('author',))
        self.assertEqual(author.modified_fields, ('articles',))

    def test_local_key_set_on_save_should_not_reset_value(self):
        article = LinkedArticle(name='A', author=None)
        article.author_id = 995
        article._set_on_save()
        self.assertEqual(article.author_id, 995)

    def test_init_should_accept_local_key(self):
        article = LKArticle(name='A', author_id=1005)
        self.assertEqual(article.author, None)
        self.assertEqual(article.author_id, 1005)

    def test_set_should_accept_local_key(self):
        article = LKArticle()
        article.set(name='A', author_id=1005)
        self.assertEqual(article.author, None)
        self.assertEqual(article.author_id, 1005)

    def test_update_should_accept_local_key(self):
        article = LKArticle()
        article.update(name='A', author_id=1005)
        self.assertEqual(article.author, None)
        self.assertEqual(article.author_id, 1005)

    def test_init_should_accept_local_key_in_json_form(self):
        article = LKArticle(**{'name': 'A', 'authorId': 1005})
        self.assertEqual(article.author, None)
        self.assertEqual(article.author_id, 1005)

    def test_set_should_accept_local_key_in_json_form(self):
        article = LKArticle()
        article.set(**{'name': 'A', 'authorId': 1005})
        self.assertEqual(article.author, None)
        self.assertEqual(article.author_id, 1005)
