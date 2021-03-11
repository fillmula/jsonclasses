from unittest import TestCase
from tests.classes.gender_user import GenderUser


class TestWriteonce(TestCase):

    def test_writeonce_cant_be_updated_by_set_if_its_value_is_present(self):
        user = GenderUser(nickname='Big Cock Brother', gender='male')
        user.set(**{'nickname': '20cm Brother', 'gender': 'female'})
        self.assertEqual(user.nickname, '20cm Brother')
        self.assertEqual(user.gender, 'male')

    def test_writeonce_can_be_updated_by_set_if_its_value_is_not_present(self):
        user = GenderUser(nickname='Alice')
        user.set(**{'nickname': 'Alice Heart', 'gender': 'female'})
        self.assertEqual(user.nickname, 'Alice Heart')
        self.assertEqual(user.gender, 'female')

    def test_writeonce_can_be_updated_by_update_anyway(self):
        user = GenderUser(nickname='Alice', gender='male')
        user.update(**{'nickname': 'Alice Heart', 'gender': 'female'})
        self.assertEqual(user.nickname, 'Alice Heart')
        self.assertEqual(user.gender, 'female')

    def test_writeonce_can_be_updated_directly_anyway(self):
        user = GenderUser(nickname='Alice', gender='male')
        user.gender = 'female'
        self.assertEqual(user.gender, 'female')
