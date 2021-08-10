from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.url_analysis import UrlAnalysis


class TestUrl(TestCase):

    def test_url_doesnt_raise_if_value_is_valid_http_url(self):
        analysis = UrlAnalysis(title='T', content='C', cover='http://google.com')
        analysis.validate()

    def test_url_doesnt_raise_if_value_is_valid_https_url(self):
        analysis = UrlAnalysis(title='T', content='C', cover='https://google.com')
        analysis.validate()

    def test_url_raises_if_value_is_not_valid_url(self):
        analysis = UrlAnalysis(title='T', content='C', cover='https://google')
        with self.assertRaises(ValidationException) as context:
            analysis.validate()
        self.assertEqual(len(context.exception.keypath_messages), 1)
        self.assertEqual(context.exception.keypath_messages['cover'],
                         "Value 'https://google' at 'cover' is not valid url.")
