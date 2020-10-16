import unittest
from jsonclasses import jsonclass, JSONObject, types


class TestInternalValidator(unittest.TestCase):

    def test_internal_fields_will_not_be_set_through_initialization(self):
        @jsonclass(class_graph='test_internal_1')
        class Secret(JSONObject):
            id: str
            secret: str = types.str.internal
        secret = Secret(id='1', secret='2')
        self.assertEqual(secret.__fdict__, {'id': '1', 'secret': None})

    def test_internal_fields_will_not_be_set_through_set_initialization(self):
        @jsonclass(class_graph='test_internal_2')
        class Secret(JSONObject):
            id: str
            secret: str = types.str.internal
        secret = Secret(id='1')
        secret.set(secret='2')
        self.assertEqual(secret.__fdict__, {'id': '1', 'secret': None})

    def test_internal_fields_can_be_set_with_update(self):
        @jsonclass(class_graph='test_internal_3')
        class Secret(JSONObject):
            id: str
            secret: str = types.str.internal
        secret = Secret(id='1')
        secret.update(secret='2')
        self.assertEqual(secret.__fdict__, {'id': '1', 'secret': '2'})

    def test_internal_fields_can_be_set_directly(self):
        @jsonclass(class_graph='test_internal_4')
        class Secret(JSONObject):
            id: str
            secret: str = types.str.internal
        secret = Secret(id='1')
        secret.secret = '2'
        self.assertEqual(secret.__fdict__, {'id': '1', 'secret': '2'})

    def test_internal_fields_will_not_be_present_in_output(self):
        @jsonclass(class_graph='test_internal_5')
        class Secret(JSONObject):
            id: str
            secret: str = types.str.internal
        secret = Secret(id='1')
        secret.secret = '2'
        self.assertEqual(secret.tojson(), {'id': '1'})
