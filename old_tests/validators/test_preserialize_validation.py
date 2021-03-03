from unittest import TestCase
from jsonclasses import jsonclass, ORMObject, types
from jsonclasses.exceptions import ValidationException
from datetime import datetime


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

    def test_preserialize_validator_should_validate_and_setonsave_inside_list(self):
        @jsonclass(class_graph='test_preserialize_validator_10')
        class User(ORMObject):
            counts: list[int] = types.listof(
                types.int.setonsave(lambda s: s + 1)
            )
        user = User(counts=[123, 456])
        user._setonsave()
        self.assertEqual(user.counts[0], 124)
        self.assertEqual(user.counts[1], 457)

    def test_preserialize_validator_should_validate_and_throw_inside_list(self):
        @jsonclass(class_graph='test_preserialize_validator_11')
        class User(ORMObject):
            counts: list[int] = types.listof(
                types.int.setonsave(lambda s: None).required
            )
        with self.assertRaises(ValidationException) as context:
            user = User(counts=[123, 456])
            user._setonsave()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['counts.0'], "Value at 'counts.0' should not be None.")

    def test_preserialize_validator_should_validate_and_setonsave_inside_dict(self):
        @jsonclass(class_graph='test_preserialize_validator_12')
        class User(ORMObject):
            counts: dict[str, int] = types.dictof(
                types.int.setonsave(lambda s: s + 1)
            )
        user = User(counts={'a': 123, 'b': 456})
        user._setonsave()
        self.assertEqual(user.counts['a'], 124)
        self.assertEqual(user.counts['b'], 457)

    def test_preserialize_validator_should_validate_and_throw_inside_dict(self):
        @jsonclass(class_graph='test_preserialize_validator_13')
        class User(ORMObject):
            counts: dict[str, int] = types.dictof(
                types.int.setonsave(lambda s: None).required
            )
        with self.assertRaises(ValidationException) as context:
            user = User(counts={'a': 123, 'b': 456})
            user._setonsave()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['counts.a'], "Value at 'counts.a' should not be None.")

    def test_preserialize_validator_should_validate_and_setonsave_inside_shape(self):
        @jsonclass(class_graph='test_preserialize_validator_14')
        class User(ORMObject):
            counts: dict[str, int] = types.shape({
                'a': types.int.setonsave(lambda x: x + 1),
                'b': types.int.setonsave(lambda x: x + 1)
            })
        user = User(counts={'a': 123, 'b': 456})
        user._setonsave()
        self.assertEqual(user.counts['a'], 124)
        self.assertEqual(user.counts['b'], 457)

    def test_preserialize_validator_should_validate_and_throw_inside_shape(self):
        @jsonclass(class_graph='test_preserialize_validator_15')
        class User(ORMObject):
            counts: dict[str, int] = types.shape({
                'a': types.int.setonsave(lambda x: x + 1),
                'b': types.int.setonsave(lambda x: None).required
            })
        with self.assertRaises(ValidationException) as context:
            user = User(counts={'a': 123, 'b': 456})
            user._setonsave()
        exception = context.exception
        self.assertEqual(exception.keypath_messages['counts.b'], "Value at 'counts.b' should not be None.")
