import unittest
from jsonclasses import jsonclass, JSONObject
from jsonclasses.graph import get_registered_class
from jsonclasses.config import Config

class TestJsonClassDecorator(unittest.TestCase):

  def test_json_class_decorator_works_alone(self):
    @jsonclass
    class MyJSONClassDecoratorTestObject(JSONObject):
      str_field: str
      int_field: str
    self.assertTrue(issubclass(MyJSONClassDecoratorTestObject, JSONObject))

  def test_json_class_decorator_works_with_graph(self):
    @jsonclass(graph='my-secret-graph-087')
    class MyJSONClassDecoratorTestObjectInMyGraph(JSONObject):
      str_field: str
      int_field: str
    self.assertTrue(issubclass(MyJSONClassDecoratorTestObjectInMyGraph, JSONObject))

  def test_json_class_decorator_without_args_raises_value_error_if_decorated_is_not_class(self):
    with self.assertRaisesRegex(ValueError, '@jsonclass should be used to decorate a class\\.'):
      @jsonclass
      def _my_method():
        pass

  def test_json_class_decorator_with_args_raises_value_error_if_decorated_is_not_class(self):
    with self.assertRaisesRegex(ValueError, '@jsonclass should be used to decorate a class\\.'):
      @jsonclass(graph='my-secret-graph-087')
      def _my_method():
        pass

  def test_json_class_decorator_without_args_raises_value_error_if_decorated_is_not_subclass_of_json_object(self):
    with self.assertRaisesRegex(ValueError, '@jsonclass should be used to decorate subclasses of JSONObject\\.'):
      @jsonclass
      class _MyOwnClass():
        pass

  def test_json_class_decorator_with_args_raises_value_error_if_decorated_is_not_subclass_of_json_object(self):
    with self.assertRaisesRegex(ValueError, '@jsonclass should be used to decorate subclasses of JSONObject\\.'):
      @jsonclass(graph='my-secret-graph-087')
      class _MyOwnClass():
        pass

  def test_json_class_decorator_without_graph_registers_class_in_default_graph(self):
    @jsonclass
    class MyJSONClassDecoratorTestObjectInDefaultGraph(JSONObject):
      str_field: str
      int_field: str
    class_from_map = get_registered_class('MyJSONClassDecoratorTestObjectInDefaultGraph', 'default')
    self.assertTrue(MyJSONClassDecoratorTestObjectInDefaultGraph is class_from_map)

  def test_json_class_decorator_with_graph_registers_class_in_designated_graph(self):
    @jsonclass(graph='my-secret-graph-087')
    class MyJSONClassDecoratorTestObjectInDefaultGraph(JSONObject):
      str_field: str
      int_field: str
    class_from_map = get_registered_class('MyJSONClassDecoratorTestObjectInDefaultGraph', 'my-secret-graph-087')
    self.assertTrue(MyJSONClassDecoratorTestObjectInDefaultGraph is class_from_map)

  def test_json_class_decorator_installs_config_on_class(self):
    @jsonclass(graph='my-secret-graph-087')
    class MyClassThatHasConfig(JSONObject):
      str_field: str
      int_field: str
    config = Config.on(MyClassThatHasConfig)
    self.assertTrue(isinstance(config, Config))
    self.assertEqual(config, Config(graph='my-secret-graph-087', camelize_json_keys=True, camelize_db_keys=True))
