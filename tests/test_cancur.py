from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.super_permission import (
    SuperPermissionArticle, SuperPermissionUser
)


class TestCanCUR(TestCase):

    def test_canc_wont_allow_if_operator_is_not_present(self):
        user = SuperPermissionUser(id=1, code=505)
        article = SuperPermissionArticle(id=2, code=504, user=user, title='1', content='2')
        with self.assertRaises(ValidationException) as context:
            article.save()
        self.assertEqual(context.exception.keypath_messages, {
            'title': 'operator not present'
        })

    def test_canc_wont_allow_if_doesnt_pass_canc_checker(self):
        user = SuperPermissionUser(id=1, code=505)
        article = SuperPermissionArticle(id=2, code=504, user=user, title='1', content='2')
        article.opby(user)
        with self.assertRaises(ValidationException) as context:
            article.save()
        self.assertEqual(context.exception.keypath_messages, {
            'title': 'operation is not permitted'
        })

    def test_canc_allows_if_passes_canc_checker(self):
        user = SuperPermissionUser(id=1, code=505)
        article = SuperPermissionArticle(id=2, code=505, user=user, title='1', content='2')
        article.opby(user)
        article.save()

    def test_canu_wont_allow_if_operator_is_not_present(self):
        user = SuperPermissionUser(id=1, code=505)
        article = SuperPermissionArticle(id=2, code=504, user=user, title='1', content='2', content2='3')
        setattr(article, "_is_new", False)
        article.content2 = '4'
        with self.assertRaises(ValidationException) as context:
            article.save(validate_all_fields=True)
        self.assertEqual(context.exception.keypath_messages, {
            'content2': 'operator not present'
        })

    def test_canu_wont_allow_if_doesnt_pass_canu_checker(self):
        user = SuperPermissionUser(id=1, code=505)
        user2 = SuperPermissionUser(id=2, code=500)
        article = SuperPermissionArticle(id=2, code=505, user=user2, title='1', content='2', content2='3')
        setattr(article, "_is_new", False)
        article.content2 = '4'
        article.opby(user)
        with self.assertRaises(ValidationException) as context:
            article.save()
        self.assertEqual(context.exception.keypath_messages, {
            'content2': 'operation is not permitted'
        })

    def test_canu_allows_if_passes_canu_checker(self):
        user = SuperPermissionUser(id=1, code=505)
        article = SuperPermissionArticle(id=2, code=505, user=user, title='1', content='2', content2='3')
        setattr(article, "_is_new", False)
        article.content2 = '4'
        article.opby(user)
        article.save()

    def test_canr_outputs_none_if_operator_is_not_present(self):
        user = SuperPermissionUser(id=1, code=505)
        article = SuperPermissionArticle(id=2, code=504, user=user, title='1', content='2')
        json = article.tojson()
        self.assertEqual(json['content'], None)

    def test_canr_outputs_none_if_doesnt_pass_canr_checker(self):
        user = SuperPermissionUser(id=1, code=505)
        article = SuperPermissionArticle(id=2, code=504, user=user, title='1', content='2')
        operator = SuperPermissionUser(id=1, code=505)
        article.opby(operator)
        json = article.tojson()
        self.assertEqual(json['content'], None)

    def test_canu_outputs_value_if_passes_canu_checker(self):
        user = SuperPermissionUser(id=1, code=505)
        article = SuperPermissionArticle(id=2, code=505, user=user, title='1', content='2')
        article.opby(user)
        json = article.tojson()
        self.assertEqual(json['content'], '2')
