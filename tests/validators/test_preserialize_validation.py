from unittest import TestCase
from jsonclasses import jsonclass, ORMObject, types
from jsonclasses.exceptions import ValidationException
from datetime import datetime, date


class TestPreserializeValidator(TestCase):

    def test_preserialize_validator_validates_on_save(self):
        @jsonclass(class_graph='test_preserialize_validator_1')
        class User(ORMObject):
            username: str
            updated_at: datetime = types.datetime.setonsave(lambda: None).required

        with self.assertRaises(ValidationException) as context:
            user = User(username='123')
            user._setonsave()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['updated_at'], "Value at 'updated_at' should not be None.")

    def test_preserialize_validator_does_not_validate_on_normal_validate(self):
        @jsonclass(class_graph='test_preserialize_validator_2')
        class User(ORMObject):
            username: str
            updated_at: datetime = types.datetime.setonsave(lambda: None).required

        user = User(username='123')
        user.validate()

    def test_preserialize_validator_does_not_raise_if_valid_on_save(self):
        @jsonclass(class_graph='test_preserialize_validator_3')
        class User(ORMObject):
            username: str
            updated_at: datetime = types.datetime.setonsave(datetime.now).required

        user = User(username='123')
        user._setonsave()

    def test_preserialize_validator_setonsave_is_chained_2(self):
        @jsonclass(class_graph='test_preserialize_validator_4')
        class User(ORMObject):
            username: str
            updated_at: int = types.datetime.setonsave(lambda: 2).setonsave(lambda x: x * 2)
        user = User(username='123')
        user._setonsave()
        self.assertEqual(user.updated_at, 4)

    def test_preserialize_validator_setonsave_is_chained_3(self):
        @jsonclass(class_graph='test_preserialize_validator_5')
        class User(ORMObject):
            username: str
            updated_at: int = types.datetime.setonsave(lambda: 2).setonsave(lambda x: x * 2).setonsave(lambda x: x + 1)
        user = User(username='123')
        user._setonsave()
        self.assertEqual(user.updated_at, 5)

    def test_preserialize_validator_validate_between_chains(self):
        @jsonclass(class_graph='test_preserialize_validator_6')
        class User(ORMObject):
            username: str
            updated_at: int = types.datetime.setonsave(lambda: 2).validate(lambda x: "wrong").setonsave(lambda x: x * 2).setonsave(lambda x: x + 1)

        with self.assertRaises(ValidationException) as context:
            user = User(username='123')
            user._setonsave()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['updated_at'], "wrong")

    def test_preserialize_validator_validate_between_chains_2(self):
        @jsonclass(class_graph='test_preserialize_validator_7')
        class User(ORMObject):
            username: str
            updated_at: int = types.datetime.setonsave(lambda: 2).setonsave(lambda x: x * 2).validate(lambda x: "wrong").setonsave(lambda x: x + 1)

        with self.assertRaises(ValidationException) as context:
            user = User(username='123')
            user._setonsave()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['updated_at'], "wrong")

    def test_preserialize_validator_validate_after_chains(self):
        @jsonclass(class_graph='test_preserialize_validator_8')
        class User(ORMObject):
            username: str
            updated_at: int = types.datetime.setonsave(lambda: 2).setonsave(lambda x: x * 2).setonsave(lambda x: x + 1).validate(lambda x: "wrong")

        with self.assertRaises(ValidationException) as context:
            user = User(username='123')
            user._setonsave()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['updated_at'], "wrong")

    def test_preserialize_validator_validate_between_chains_do_not_throw_if_valid(self):
        @jsonclass(class_graph='test_preserialize_validator_9')
        class User(ORMObject):
            username: str
            updated_at: int = types.datetime \
                                   .setonsave(lambda: 2).validate(lambda x: None) \
                                   .setonsave(lambda x: x * 2).validate(lambda x: None) \
                                   .setonsave(lambda x: x + 1).validate(lambda x: None)

        user = User(username='123')
        user._setonsave()


    # def test_eager_validator_will_not_perform_when_value_is_none_on_init(self):
    #     @jsonclass(class_graph='test_eager_validator_3')
    #     class User(JSONObject):
    #         username: str = types.str.required
    #         password: str = types.str.minlength(8).maxlength(16).transform(lambda s: s + '0x0x').required
    #     try:
    #         _user = User()
    #     except ValidationException:
    #         self.fail('eager validator should not perform on init if value is None.')


    # def test_eager_validator_should_validate_and_transform_inside_list(self):
    #     @jsonclass(class_graph='test_eager_validator_7')
    #     class User(JSONObject):
    #         passwords: list[str] = types.listof(
    #             types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
    #         )
    #     try:
    #         _user = User(passwords=['123', '456', '789', '012'])
    #     except:
    #         self.fail('eager validator should not throw if value is valid')

    # def test_eager_validator_should_validate_and_throw_inside_list(self):
    #     @jsonclass(class_graph='test_eager_validator_8')
    #     class User(JSONObject):
    #         passwords: list[str] = types.listof(
    #             types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
    #         )
    #     with self.assertRaises(ValidationException):
    #         _user = User(passwords=['123xxx', '456xxx', '789xxx', '012xxx'])

    # def test_eager_validator_should_validate_and_transform_inside_dict(self):
    #     @jsonclass(class_graph='test_eager_validator_9')
    #     class User(JSONObject):
    #         passwords: dict[str, str] = types.dictof(
    #             types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
    #         )
    #     try:
    #         _user = User(passwords={'a': '123', 'b': '456', 'c': '789', 'd': '012'})
    #     except:
    #         self.fail('eager validator should not throw if value is valid')

    # def test_eager_validator_should_validate_and_throw_inside_dict(self):
    #     @jsonclass(class_graph='test_eager_validator_10')
    #     class User(JSONObject):
    #         passwords: dict[str, str] = types.dictof(
    #             types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
    #         )
    #     with self.assertRaises(ValidationException):
    #         _user = User(passwords={'a': '123xxx', 'b': '456xxx', 'c': '789xxx', 'd': '012xxx'})

    # def test_eager_validator_should_validate_and_transform_inside_shape(self):
    #     @jsonclass(class_graph='test_eager_validator_11')
    #     class User(JSONObject):
    #         passwords: dict[str, str] = types.shape({
    #             'a': types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x'),
    #             'b': types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
    #         })
    #     try:
    #         _user = User(passwords={'a': '123', 'b': '456'})
    #     except:
    #         self.fail('eager validator should not throw if value is valid')

    # def test_eager_validator_should_validate_and_throw_inside_shape(self):
    #     @jsonclass(class_graph='test_eager_validator_12')
    #     class User(JSONObject):
    #         passwords: dict[str, str] = types.shape({
    #             'a': types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x'),
    #             'b': types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
    #         })
    #     with self.assertRaises(ValidationException):
    #         _user = User(passwords={'a': '123xxx', 'b': '456xxx'})

    # def test_eager_validator_should_lazy_validate_when_validate_inside_list(self):
    #     @jsonclass(class_graph='test_eager_validator_13')
    #     class User(JSONObject):
    #         passwords: list[str] = types.listof(
    #             types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
    #         )
    #     user = User(passwords=['123', '456', '789', '012'])
    #     try:
    #         user.validate()
    #     except:
    #         self.fail('eager validator should not throw if not validation task after eager mark')

    # def test_eager_validator_should_lazy_validate_when_validate_inside_dict(self):
    #     @jsonclass(class_graph='test_eager_validator_14')
    #     class User(JSONObject):
    #         passwords: dict[str, str] = types.dictof(
    #             types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
    #         )
    #     user = User(passwords={'a': '123', 'b': '456', 'c': '789', 'd': '012'})
    #     try:
    #         user.validate()
    #     except:
    #         self.fail('eager validator should not throw if not validation task after eager mark')

    # def test_eager_validator_should_lazy_validate_when_validate_inside_shape(self):
    #     @jsonclass(class_graph='test_eager_validator_15')
    #     class User(JSONObject):
    #         passwords: dict[str, str] = types.shape({
    #             'a': types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x'),
    #             'b': types.str.minlength(2).maxlength(4).transform(lambda s: s + '0x0x0x0x')
    #         })
    #     user = User(passwords={'a': '123', 'b': '456'})
    #     try:
    #         user.validate()
    #     except:
    #         self.fail('eager validator should not throw if not validation task after eager mark')
