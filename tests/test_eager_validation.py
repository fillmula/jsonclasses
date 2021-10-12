from unittest import TestCase
from jsonclasses.excs import ValidationException
from tests.classes.ev_user import EvUser, EvUserL, EvUserD


class TestEagerValidation(TestCase):

    def test_eager_modifier_validates_on_init(self):
        with self.assertRaises(ValidationException) as context:
            EvUser(password='123')
        self.assertEqual("length of value is not greater than or equal 8",
                         context.exception.keypath_messages['password'])

    def test_eager_modifier_doesnt_cause_other_fields_to_validate_on_init(self):
        user = EvUser(password='12345678')
        self.assertEqual(user._data_dict, {'username': None, 'password': '123456780x0x'})

    def test_eager_modifier_will_not_perform_when_value_is_none_on_init(self):
        try:
            EvUser()
        except ValidationException:
            self.fail('eager modifier should not perform on init if value is None.')

    def test_eager_modifier_validates_on_set(self):
        user = EvUser()
        with self.assertRaises(ValidationException) as context:
            user.set(password='123')
        self.assertEqual("length of value is not greater than or equal 8",
                         context.exception.keypath_messages['password'])

    def test_eager_modifier_will_not_work_on_update(self):
        user = EvUser()
        try:
            user.update(password='123')
        except ValidationException:
            self.fail('eager modifier should not perform on update.')

    def test_eager_modifier_prevents_modifiers_before_it_on_validate(self):
        user = EvUser(password='1234567890123456', username='Tsi')
        try:
            user.validate()
        except ValidationException:
            self.fail('eager modifier should prevent modifiers before it to work on validate.')

    def test_eager_modifier_should_work_inside_list(self):
        try:
            EvUserL(passwords=['123', '456', '789', '012'])
        except ValidationException:
            self.fail('eager modifier should not throw if value is valid')

    def test_eager_modifier_should_throw_inside_list(self):
        with self.assertRaises(ValidationException):
            EvUserL(passwords=['123xxx', '456xxx', '789xxx', '012xxx'])

    def test_eager_modifier_should_work_inside_dict(self):
        try:
            EvUserD(passwords={'a': '123', 'b': '456', 'c': '789', 'd': '012'})
        except ValidationException:
            self.fail('eager modifier should not throw if value is valid')

    def test_eager_modifier_should_validate_and_throw_inside_dict(self):
        with self.assertRaises(ValidationException):
            EvUserD(passwords={'a': '123xxx', 'b': '456xxx', 'c': '789xxx',
                               'd': '012xxx'})

    def test_eager_modifier_should_lazy_validate_when_validate_inside_list(self):
        user = EvUserL(passwords=['123', '456', '789', '012'])
        try:
            user.validate()
        except ValidationException:
            self.fail('eager modifier should not throw if not validation task after eager mark')

    def test_eager_modifier_should_lazy_validate_when_validate_inside_dict(self):
        user = EvUserD(passwords={'a': '123', 'b': '456', 'c': '789', 'd': '012'})
        try:
            user.validate()
        except ValidationException:
            self.fail('eager modifier should not throw if not validation task after eager mark')
