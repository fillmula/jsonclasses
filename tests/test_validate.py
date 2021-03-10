from __future__ import annotations
from unittest import TestCase
from jsonclasses.exceptions import ValidationException
from tests.classes.simple_article import SimpleArticle
from tests.classes.simple_language import SimpleLanguage
from tests.classes.simple_project import SimpleProject
from tests.classes.simple_chart import SimpleChart
from tests.classes.simple_setting import SimpleSetting
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
                         "Value at 'title' should not be None.")

    def test_validate_validates_all_fields_if_option_is_passed(self):
        article = SimpleArticle()
        with self.assertRaises(ValidationException) as context:
            article.validate(validate_all_fields=True)
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 2)
        self.assertEqual(exception.keypath_messages['title'],
                         "Value at 'title' should not be None.")
        self.assertEqual(exception.keypath_messages['content'],
                         "Value at 'content' should not be None.")

    def test_validate_validates_all_fields_if_class_config_is_on(self):
        language = SimpleLanguage()
        with self.assertRaises(ValidationException) as context:
            language.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 2)
        self.assertEqual(exception.keypath_messages['name'],
                         "Value at 'name' should not be None.")
        self.assertEqual(exception.keypath_messages['code'],
                         "Value at 'code' should not be None.")

    def test_validate_validates_one_field_if_explicitly_specified(self):
        language = SimpleLanguage()
        with self.assertRaises(ValidationException) as context:
            language.validate(validate_all_fields=False)
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['name'],
                         "Value at 'name' should not be None.")

    def test_validate_validates_one_list_field_by_default(self):
        project = SimpleProject(name='Teo', attendees=['A', 'B', 'C', 'D'])
        with self.assertRaises(ValidationException) as context:
            project.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['attendees.0'],
                         "Length of value 'A' at 'attendees.0' should not be "
                         "less than 2.")

    def test_validate_validates_all_list_fields_if_required(self):
        project = SimpleProject(name='Teo', attendees=['A', 'B', 'C', 'D'])
        with self.assertRaises(ValidationException) as context:
            project.validate(validate_all_fields=True)
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 4)
        self.assertEqual(exception.keypath_messages['attendees.0'],
                         "Length of value 'A' at 'attendees.0' should not be "
                         "less than 2.")
        self.assertEqual(exception.keypath_messages['attendees.1'],
                         "Length of value 'B' at 'attendees.1' should not be "
                         "less than 2.")
        self.assertEqual(exception.keypath_messages['attendees.2'],
                         "Length of value 'C' at 'attendees.2' should not be "
                         "less than 2.")
        self.assertEqual(exception.keypath_messages['attendees.3'],
                         "Length of value 'D' at 'attendees.3' should not be "
                         "less than 2.")

    def test_validate_validates_one_dict_field_by_default(self):
        chart = SimpleChart(name='Teo', partitions={
            'a': 2, 'b': 3, 'c': 4, 'd': 5})
        with self.assertRaises(ValidationException) as context:
            chart.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['partitions.a'],
                         "Value '2.0' at 'partitions.a' should not be "
                         "greater than 1.")

    def test_validate_validates_all_dict_fields_if_required(self):
        chart = SimpleChart(name='Teo', partitions={
            'a': 2, 'b': 3, 'c': 4, 'd': 5})
        with self.assertRaises(ValidationException) as context:
            chart.validate(validate_all_fields=True)
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 4)
        self.assertEqual(exception.keypath_messages['partitions.a'],
                         "Value '2.0' at 'partitions.a' should not be "
                         "greater than 1.")
        self.assertEqual(exception.keypath_messages['partitions.b'],
                         "Value '3.0' at 'partitions.b' should not be "
                         "greater than 1.")
        self.assertEqual(exception.keypath_messages['partitions.c'],
                         "Value '4.0' at 'partitions.c' should not be "
                         "greater than 1.")
        self.assertEqual(exception.keypath_messages['partitions.d'],
                         "Value '5.0' at 'partitions.d' should not be "
                         "greater than 1.")

    def test_validate_validates_one_field_inside_shape_by_default(self):
        setting = SimpleSetting(
            user='A',
            email={'auto_send': 'A', 'receive_promotion': 'B'})
        with self.assertRaises(ValidationException) as context:
            setting.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['email.auto_send'],
                         "Value 'A' at 'email.auto_send' should be bool.")

    def test_validate_validates_all_fields_inside_shape_if_required(self):
        setting = SimpleSetting(
            user='A',
            email={'auto_send': 'A', 'receive_promotion': 'B'})
        with self.assertRaises(ValidationException) as context:
            setting.validate(validate_all_fields=True)
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 2)
        self.assertEqual(exception.keypath_messages['email.auto_send'],
                         "Value 'A' at 'email.auto_send' should be bool.")
        self.assertEqual(exception.keypath_messages['email.receive_promotion'],
                         "Value 'B' at 'email.receive_promotion' should be "
                         "bool.")

    def test_validate_validates_with_class_config_by_default(self):
        author = Author(name='A', articles=[{}, {}])
        with self.assertRaises(ValidationException) as context:
            author.validate()
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 2)
        self.assertEqual(exception.keypath_messages['articles.0.title'],
                         "Value at 'articles.0.title' should not be None.")
        self.assertEqual(exception.keypath_messages['articles.0.content'],
                         "Value at 'articles.0.content' should not be None.")

    def test_validate_validates_one_field_inside_nested_if_required(self):
        author = Author(name='A', articles=[{}, {}])
        with self.assertRaises(ValidationException) as context:
            author.validate(validate_all_fields=False)
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 1)
        self.assertEqual(exception.keypath_messages['articles.0.title'],
                         "Value at 'articles.0.title' should not be None.")

    def test_validate_validates_all_field_inside_nested_if_required(self):
        author = Author(name='A', articles=[{}, {}])
        with self.assertRaises(ValidationException) as context:
            author.validate(validate_all_fields=True)
        exception = context.exception
        self.assertEqual(len(exception.keypath_messages), 4)
        self.assertEqual(exception.keypath_messages['articles.0.title'],
                         "Value at 'articles.0.title' should not be None.")
        self.assertEqual(exception.keypath_messages['articles.0.content'],
                         "Value at 'articles.0.content' should not be None.")
        self.assertEqual(exception.keypath_messages['articles.1.title'],
                         "Value at 'articles.1.title' should not be None.")
        self.assertEqual(exception.keypath_messages['articles.1.content'],
                         "Value at 'articles.1.content' should not be None.")

    def test_validate_only_validate_modified_fields_for_non_new_object(self):
        article = SimpleArticle(title='my', content='side')
        article._mark_not_new()
        article.content = None
        article._modified_fields = []
        article.validate(validate_all_fields=True)

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
                         "Value at 'articles.0.content' should not be None.")

    def test_validate_linked_objects_no_infinite_loop(self):
        profile = LinkedProfile(name='Ua Bê Tshiu Pên')
        user = LinkedUser(name='Tsuan Sê Kai')
        user.profile = profile
        user.validate()
