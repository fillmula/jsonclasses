from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import JSONClassResetNotEnabledError
from tests.classes.resetable_score import ResetableScore
from tests.classes.simple_article import SimpleArticle


class TestReset(TestCase):

    def test_reset_primitive_field(self):
        score = ResetableScore(name='today', total=95)
        score._mark_not_new()
        score.name = 'yesterday'
        score.reset()
        self.assertEqual(score.name, 'today')
        self.assertEqual(score.is_modified, False)
        self.assertEqual(score.modified_fields, ())

    def test_reset_list(self):
        score = ResetableScore(name='today', total=95, scores=[80, 70, 100])
        score._mark_not_new()
        score.scores = [100, 90, 80]
        score.reset()
        self.assertEqual(score.scores, [80, 70, 100])
        self.assertEqual(score.is_modified, False)
        self.assertEqual(score.modified_fields, ())

    def test_reset_dict(self):
        score = ResetableScore(name='today', total=95, history={'y': 4})
        score._mark_not_new()
        score.history['q'] = 5
        score.reset()
        self.assertEqual(score.history, {'y': 4})
        self.assertEqual(score.is_modified, False)
        self.assertEqual(score.modified_fields, ())

    def test_reset_wont_record_if_no_reset_all_fields_option(self):
        article = SimpleArticle(title='q', content='b')
        article._mark_not_new()
        article.title = 'a'
        article.title = 'b'
        self.assertEqual(article.previous_values, {})

    def test_reset_raises_if_no_reset_all_fields_option(self):
        article = SimpleArticle(title='q', content='b')
        article._mark_not_new()
        article.title = 'a'
        article.title = 'b'
        with self.assertRaises(JSONClassResetNotEnabledError):
            article.reset()
