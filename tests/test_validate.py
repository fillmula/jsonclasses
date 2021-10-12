from __future__ import annotations
from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.simple_article import SimpleArticle
from tests.classes.simple_language import SimpleLanguage
from tests.classes.simple_project import SimpleProject
from tests.classes.simple_chart import SimpleChart
from tests.classes.author import Author
from tests.classes.linked_profile import LinkedProfile
from tests.classes.linked_user import LinkedUser


class TestValidate(TestCase):

    def test_validate_does_not_raise_and_returns_self_for_valid_object(self):
        article = SimpleArticle(title='U Ia Huê', content='Bê Tshua Bo')
        self.assertEqual(article, article.validate())

    def test_validate_raises_if_object_is_not_valid(self):
        article = SimpleArticle()
        self.assertRaises(ValidationException, article.validate)

    def test_is_valid_returns_false_if_object_is_not_valid(self):
        article = SimpleArticle()
        self.assertEqual(False, article.is_valid)

    def test_is_valid_returns_true_if_object_is_valid(self):
        article = SimpleArticle(title='U Ia Huê', content='Bê Tshua Bo')
        self.assertEqual(True, article.is_valid)

    def test_validate_by_default_validates_one_field(self):
        article = SimpleArticle()
        with self.assertRaises(ValidationException) as context:
            article.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['title'],
                         "value required")

    def test_validate_validates_all_fields_if_option_is_passed(self):
        article = SimpleArticle()
        with self.assertRaises(ValidationException) as context:
            article.validate(all_fields=True)
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 2)
        self.assertEqual(exception.keypath_messages['title'],
                         "value required")
        self.assertEqual(exception.keypath_messages['content'],
                         "value required")

    def test_validate_validates_all_fields_if_class_config_is_on(self):
        language = SimpleLanguage()
        with self.assertRaises(ValidationException) as context:
            language.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 2)
        self.assertEqual(exception.keypath_messages['name'],
                         "value required")
        self.assertEqual(exception.keypath_messages['code'],
                         "value required")

    def test_validate_validates_one_field_if_explicitly_specified(self):
        language = SimpleLanguage()
        with self.assertRaises(ValidationException) as context:
            language.validate(all_fields=False)
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['name'],
                         "value required")

    def test_validate_validates_one_list_field_by_default(self):
        project = SimpleProject(name='Teo', attendees=['A', 'B', 'C', 'D'])
        with self.assertRaises(ValidationException) as context:
            project.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['attendees.0'],
                         "length of value is not greater than or equal 2")

    def test_validate_validates_all_list_fields_if_required(self):
        project = SimpleProject(name='Teo', attendees=['A', 'B', 'C', 'D'])
        with self.assertRaises(ValidationException) as context:
            project.validate(all_fields=True)
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 4)
        self.assertEqual(exception.keypath_messages['attendees.0'],
                         "length of value is not greater than or equal 2")
        self.assertEqual(exception.keypath_messages['attendees.1'],
                         "length of value is not greater than or equal 2")
        self.assertEqual(exception.keypath_messages['attendees.2'],
                         "length of value is not greater than or equal 2")
        self.assertEqual(exception.keypath_messages['attendees.3'],
                         "length of value is not greater than or equal 2")

    def test_validate_validates_one_dict_field_by_default(self):
        chart = SimpleChart(name='Teo', partitions={
            'a': 2, 'b': 3, 'c': 4, 'd': 5})
        with self.assertRaises(ValidationException) as context:
            chart.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['partitions.a'],
                         "value is not less than or equal 1")

    def test_validate_validates_all_dict_fields_if_required(self):
        chart = SimpleChart(name='Teo', partitions={
            'a': 2, 'b': 3, 'c': 4, 'd': 5})
        with self.assertRaises(ValidationException) as context:
            chart.validate(all_fields=True)
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 4)
        self.assertEqual(exception.keypath_messages['partitions.a'],
                         "value is not less than or equal 1")
        self.assertEqual(exception.keypath_messages['partitions.b'],
                         "value is not less than or equal 1")
        self.assertEqual(exception.keypath_messages['partitions.c'],
                         "value is not less than or equal 1")
        self.assertEqual(exception.keypath_messages['partitions.d'],
                         "value is not less than or equal 1")

    def test_validate_validates_with_class_config_by_default(self):
        author = Author(name='A', articles=[{}, {}])
        with self.assertRaises(ValidationException) as context:
            author.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 2)
        self.assertEqual(exception.keypath_messages['articles.0.title'],
                         "value required")
        self.assertEqual(exception.keypath_messages['articles.0.content'],
                         "value required")

    def test_validate_validates_one_field_inside_nested_if_required(self):
        author = Author(name='A', articles=[{}, {}])
        with self.assertRaises(ValidationException) as context:
            author.validate(all_fields=False)
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['articles.0.title'],
                         "value required")

    def test_validate_validates_all_field_inside_nested_if_required(self):
        author = Author(name='A', articles=[{}, {}])
        with self.assertRaises(ValidationException) as context:
            author.validate(all_fields=True)
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 4)
        self.assertEqual(exception.keypath_messages['articles.0.title'],
                         "value required")
        self.assertEqual(exception.keypath_messages['articles.0.content'],
                         "value required")
        self.assertEqual(exception.keypath_messages['articles.1.title'],
                         "value required")
        self.assertEqual(exception.keypath_messages['articles.1.content'],
                         "value required")

    def test_validate_only_validate_modified_fields_for_non_new_object(self):
        article = SimpleArticle(title='my', content='side')
        article._mark_not_new()
        article.content = None
        article._modified_fields = []
        article.validate(all_fields=True)

    def test_validate_validates_linked_objects_anyway(self):
        author = Author(name='Tsit Tiu',
                        articles=[{'title': 'Khua Tioh Sê Kai',
                                   'content': 'Ai Gua Tsuê'},
                                  {'title': 'Thên Ha Si Lan Ê',
                                   'content': 'Tsiu Ho Lang Tsai'}])
        author._mark_not_new()
        author.articles[0]._mark_not_new()
        author.articles[1]._mark_not_new()
        author.articles[0].content = None
        with self.assertRaises(ValidationException) as context:
            author.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['articles.0.content'],
                         "value required")

    def test_validate_linked_objects_no_infinite_loop(self):
        profile = LinkedProfile(name='Ua Bê Tshiu Pên')
        user = LinkedUser(name='Tsuan Sê Kai')
        user.profile = profile
        user.validate()
