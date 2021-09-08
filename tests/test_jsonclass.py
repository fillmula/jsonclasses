from __future__ import annotations
from unittest import TestCase
from jsonclasses import jsonclass
from jsonclasses.isjsonclass import isjsonclass
from jsonclasses.jconf import JConf
from jsonclasses.keypath import (
    camelize_key, identical_key, reference_key, underscore_key
)
from jsonclasses.cgraph import CGraph
from jsonclasses.excs import JSONClassRedefinitionException
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
        class_config = SimpleAccount.cdef.jconf
        default_config = JConf(cgraph='default',
                                key_encoding_strategy=camelize_key,
                                key_decoding_strategy=underscore_key,
                                strict_input=True,
                                ref_key_encoding_strategy=reference_key,
                                validate_all_fields=False,
                                abstract=False,
                                reset_all_fields=False,
                                on_create=[],
                                on_update=[],
                                on_delete=[],
                                can_create=[],
                                can_update=[],
                                can_delete=[],
                                can_read=[])
        self.assertEqual(class_config, default_config)

    def test_jsonclass_cgraph_changes_cgraph(self):
        cgraph = SimpleCompany.cdef.jconf.cgraph
        company_graph = CGraph('simplecompany')
        self.assertEqual(cgraph, company_graph)

    def test_jsonclass_key_encoding_strategy_changes_config(self):
        self.assertEqual(
            SimpleEmployee.cdef.jconf.key_encoding_strategy, identical_key)

    def test_jsonclass_key_decoding_strategy_changes_config(self):
        self.assertEqual(
            SimpleEmployee.cdef.jconf.key_decoding_strategy, identical_key)

    def test_jsonclass_strict_input_changes_config(self):
        self.assertEqual(
            SimpleEmployee.cdef.jconf.strict_input, False)

    def test_jsonclass_key_transformer_changes_config(self):
        self.assertEqual(
            SimpleEmployee.cdef.jconf.ref_key_encoding_strategy,
            yet_another_key_transformer)

    def test_jsonclass_validate_all_fields_changes_config(self):
        self.assertEqual(
            SimpleEmployee.cdef.jconf.validate_all_fields, True)

    def test_jsonclass_abstract_changes_config(self):
        self.assertEqual(
            SimpleEmployee.cdef.jconf.abstract, True)

    def test_jsonclass_reset_all_fields_changes_config(self):
        self.assertEqual(
            SimpleEmployee.cdef.jconf.reset_all_fields, True)

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
