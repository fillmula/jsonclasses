from __future__ import annotations
from unittest import TestCase
from jsonclasses import jsonclass
from jsonclasses.isjsonclass import isjsonclass
from jsonclasses.config import Config
from jsonclasses.keypath_utils import reference_key
from jsonclasses.jsonclass_graph import JSONClassGraph
from jsonclasses.exceptions import JSONClassRedefinitionException
from tests.classes.simple_account import SimpleAccount
from tests.classes.simple_company import SimpleCompany
from tests.classes.simple_employee import SimpleEmployee
from tests.funcs.yet_another_key_transformer import yet_another_key_transformer


class TestJsonClass(TestCase):

    def test_jsonclass_returns_jsonclass_without_arguments(self):
        self.assertTrue(isjsonclass(SimpleAccount))

    def test_jsonclass_returns_jsonclass_with_arguments(self):
        self.assertTrue(isjsonclass(SimpleCompany))

    def test_jsonclass_install_default_config_without_arguments(self):
        class_config = SimpleAccount.definition.config
        default_config = Config(class_graph='default',
                                camelize_json_keys=True,
                                strict_input=True,
                                key_transformer=reference_key,
                                validate_all_fields=False,
                                soft_delete=False,
                                abstract=False,
                                reset_all_fields=False,
                                on_create=[],
                                on_save=[],
                                on_delete=[],
                                can_create=[],
                                can_update=[],
                                can_delete=[],
                                can_read=[])
        self.assertEqual(class_config, default_config)

    def test_jsonclass_class_graph_changes_class_graph(self):
        class_graph = SimpleCompany.definition.config.class_graph
        company_graph = JSONClassGraph('simplecompany')
        self.assertEqual(class_graph, company_graph)

    def test_jsonclass_camelize_json_keys_changes_config(self):
        self.assertEqual(
            SimpleEmployee.definition.config.camelize_json_keys, False)

    def test_jsonclass_strict_input_changes_config(self):
        self.assertEqual(
            SimpleEmployee.definition.config.strict_input, False)

    def test_jsonclass_key_transformer_changes_config(self):
        self.assertEqual(
            SimpleEmployee.definition.config.key_transformer,
            yet_another_key_transformer)

    def test_jsonclass_validate_all_fields_changes_config(self):
        self.assertEqual(
            SimpleEmployee.definition.config.validate_all_fields, True)

    def test_jsonclass_soft_delete_changes_config(self):
        self.assertEqual(
            SimpleEmployee.definition.config.soft_delete, True)

    def test_jsonclass_abstract_changes_config(self):
        self.assertEqual(
            SimpleEmployee.definition.config.abstract, True)

    def test_jsonclass_reset_all_fields_changes_config(self):
        self.assertEqual(
            SimpleEmployee.definition.config.reset_all_fields, True)

    def test_jsonclass_raises_value_error_if_decorated_is_not_class(self):
        with self.assertRaisesRegex(ValueError, '@jsonclass should be used to'
                                                ' decorate a class\\.'):
            @jsonclass
            def _my_method():
                pass

    def test_jsonclass_raises_if_duplicate_names_on_same_graph(self):
        with self.assertRaisesRegex(JSONClassRedefinitionException,
                                    'jsonclass name conflict in graph'):
            @jsonclass(class_graph='simplecompany')
            class SimpleCompany:
                str_field: str
                int_field: str
