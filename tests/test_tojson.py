from unittest import TestCase
from tests.classes.simple_deadline import SimpleDeadline
from tests.classes.simple_account import SimpleAccount
from tests.classes.linked_profile import LinkedProfile
from tests.classes.linked_user import LinkedUser


class TestToJson(TestCase):

    def test_tojson_auto_camelize_keys_by_default(self):
        deadline = SimpleDeadline(ended_at='2021-03-04')
        self.assertEqual(
            deadline.tojson(),
            {'endedAt': '2021-03-04T00:00:00.000Z', 'message': None})

    def test_tojson_remove_writeonly_keys_by_default(self):
        account = SimpleAccount(username='inmylife', password='iloveyoumore')
        self.assertEqual(account.tojson(), {'username': 'inmylife'})

    def test_tojson_do_not_remove_writeonly_keys_if_specified(self):
        account = SimpleAccount(username='dobusiness', password='earnbigmoney')
        self.assertEqual(account.tojson(ignore_writeonly=True),
                         {'username': 'dobusiness',
                          'password': 'earnbigmoney'})

    def test_tojson_linked_objects_do_not_go_to_infinite_loop(self):
        profile = LinkedProfile(name='Tsit Po Po')
        user = LinkedUser(name='Kia Tsiu Tai')
        user.profile = profile
        self.assertEqual(user.tojson(),
                         {'name': 'Kia Tsiu Tai',
                          'profile': {'name': 'Tsit Po Po',
                                      'user': {'name': 'Kia Tsiu Tai'}}})
