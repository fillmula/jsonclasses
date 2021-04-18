from typing import Optional, Union
from unittest import TestCase
from datetime import datetime, date
from jsonclasses import jsonclass
from jsonclasses.field_definition import FieldType, FieldStorage
from jsonclasses.exceptions import ValidationException
from tests.classes.linked_author import LinkedAuthor
from tests.classes.linked_article import LinkedArticle
from tests.classes.linked_user import LinkedUser
from tests.classes.linked_product import LinkedProduct
from tests.classes.linked_customer import LinkedCustomer
from tests.classes.linked_profile import LinkedProfile
from tests.classes.auto_setting import AutoSetting
from tests.classes.auto_str_setting import AutoStrSetting


class TestAutoTypes(TestCase):

    def test_auto_generates_required_str(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestStr:
            val: str
        object = TestStr()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_str(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalStr:
            val: Optional[str]
        object = TestOptionalStr()
        object.validate()

    def test_auto_generates_required_str_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestStrStrType:
            val: 'str'
        object = TestStrStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_str_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalStrStrType:
            val: 'Optional[str]'
        object = TestOptionalStrStrType()
        object.validate()

    def test_auto_generates_required_int(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestInt:
            val: int
        object = TestInt()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_int(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalInt:
            val: Optional[int]
        object = TestOptionalInt()
        object.validate()

    def test_auto_generates_required_int_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestIntStrType:
            val: 'int'
        object = TestIntStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_int_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalIntStrType:
            val: 'Optional[int]'
        object = TestOptionalIntStrType()
        object.validate()

    def test_auto_generates_required_float(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestFloat:
            val: float
        object = TestFloat()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_float(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalfloat:
            val: Optional[float]
        object = TestOptionalfloat()
        object.validate()

    def test_auto_generates_required_float_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestFloatStrType:
            val: 'float'
        object = TestFloatStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_float_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalFloatStrType:
            val: 'Optional[float]'
        object = TestOptionalFloatStrType()
        object.validate()

    def test_auto_generates_required_bool(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestBool:
            val: bool
        object = TestBool()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_bool(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalbool:
            val: Optional[bool]
        object = TestOptionalbool()
        object.validate()

    def test_auto_generates_required_bool_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestboolStrType:
            val: 'bool'
        object = TestboolStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_bool_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalboolStrType:
            val: 'Optional[bool]'
        object = TestOptionalboolStrType()
        object.validate()

    def test_auto_generates_required_date(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class Testdate:
            val: date
        object = Testdate()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_date(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionaldate:
            val: Optional[date]
        object = TestOptionaldate()
        object.validate()

    def test_auto_generates_required_date_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestdateStrType:
            val: 'date'
        object = TestdateStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_date_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionaldateStrType:
            val: 'Optional[date]'
        object = TestOptionaldateStrType()
        object.validate()

    def test_auto_generates_required_datetime(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class Testdatetime:
            val: datetime
        object = Testdatetime()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_datetime(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionaldatetime:
            val: Optional[datetime]
        object = TestOptionaldatetime()
        object.validate()

    def test_auto_generates_required_datetime_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestdatetimeStrType:
            val: 'datetime'
        object = TestdatetimeStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_datetime_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionaldatetimeStrType:
            val: 'Optional[datetime]'
        object = TestOptionaldatetimeStrType()
        object.validate()

    def test_auto_generates_required_list(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class Testlist:
            val: list[str]
        object = Testlist()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_list(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class TestOptionallist:
            val: Optional[list[str]]
        object = TestOptionallist()
        object.validate()

    def test_auto_generates_required_list_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class TestlistStrType:
            val: 'list[str]'
        object = TestlistStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_list_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class TestOptionallistStrType:
            val: 'Optional[list[str]]'
        object = TestOptionallistStrType()
        object.validate()

    def test_auto_generates_required_list_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class Testlist:
            val: list[str]
        object = Testlist()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_list_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionallist:
            val: Optional[list[str]]
        object = TestOptionallist()
        object.validate()

    def test_auto_generates_required_list_with_str_type_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestlistStrType:
            val: 'list[str]'
        object = TestlistStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_list_with_str_type_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionallistStrType:
            val: 'Optional[list[str]]'
        object = TestOptionallistStrType()
        object.validate()

    def test_auto_generates_required_dict(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class Testdict:
            val: dict[str, str]
        object = Testdict()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_dict(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class TestOptionaldict:
            val: Optional[dict[str, str]]
        object = TestOptionaldict()
        object.validate()

    def test_auto_generates_required_dict_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class TestdictStrType:
            val: 'dict[str, str]'
        object = TestdictStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_dict_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class TestOptionaldictStrType:
            val: 'Optional[dict[str, str]]'
        object = TestOptionaldictStrType()
        object.validate()

    def test_auto_generates_required_dict_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class Testdict:
            val: dict[str, str]
        object = Testdict()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_dict_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionaldict:
            val: Optional[dict[str, str]]
        object = TestOptionaldict()
        object.validate()

    def test_auto_generates_required_dict_with_str_type_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestdictStrType:
            val: 'dict[str, str]'
        object = TestdictStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_dict_with_str_type_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionaldictStrType:
            val: 'Optional[dict[str, str]]'
        object = TestOptionaldictStrType()
        object.validate()

    def test_auto_generates_required_instance(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestinstanceReferenced:
            val: Optional[str]

        @jsonclass(class_graph='test_marker_auto_gen')
        class Testinstance:
            val: TestinstanceReferenced
        object = Testinstance()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_instance(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestoptionalinstanceReferenced:
            val: Optional[str]

        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalInstance:
            val: Optional[TestoptionalinstanceReferenced]
        object = TestOptionalInstance()
        object.validate()

    def test_auto_generates_required_instance_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestinstanceReferencedWithStrType:
            val: Optional[str]

        @jsonclass(class_graph='test_marker_auto_gen')
        class TestinstanceWithStrType:
            val: 'TestinstanceReferencedWithStrType'
        object = TestinstanceWithStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_instance_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestoptionalinstanceReferencedWithStrType:
            val: Optional[str]

        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalInstanceWithStrType:
            val: 'Optional[TestoptionalinstanceReferencedWithStrType]'
        object = TestOptionalInstanceWithStrType()
        object.validate()

    def test_auto_generates_required_union(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestUnion:
            val: Union[str, bool]
        object = TestUnion()
        self.assertFalse(object.is_valid)

    def test_auto_generates_optional_union(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalUnion:
            val: Optional[Union[str, bool]]
        object = TestOptionalUnion()
        object.validate()

    def test_auto_generates_required_union_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestUnionStrType:
            val: 'Union[str, int]'
        object = TestUnionStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_union_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalUnionStrType:
            val: 'Optional[Union[int, float]]'
        object = TestOptionalUnionStrType()
        object.validate()

    def test_auto_generates_required_union_with_dict_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestUnionDictType:
            val: 'Union[dict[str, int], int]'
        cfield = TestUnionDictType.definition.field_named('val')
        utypes = cfield.definition.union_types
        self.assertEqual(utypes[0].definition.field_type, FieldType.DICT)
        self.assertEqual(utypes[1].definition.field_type, FieldType.INT)

    def test_auto_generates_optional_union_with_dict_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalUnionDictType:
            val: 'Optional[Union[dict[str, bool], float]]'
        object = TestOptionalUnionDictType()
        object.validate()

    def test_auto_generates_nonnull_shape_with_typed_dict(self):
        setting = AutoSetting()
        self.assertRaisesRegex(
            ValidationException,
            "Value at 'preference.ios' should not be None.",
            setting.validate)

    def test_auto_generates_nonnull_shape_with_typed_dict_str_form(self):
        setting = AutoStrSetting()
        self.assertRaisesRegex(
            ValidationException,
            "Value at 'preference.ios' should not be None.",
            setting.validate)

    def test_auto_generates_1_to_1_links(self):
        profile_field = LinkedUser.definition.field_named('profile')
        self.assertEqual(profile_field.definition.field_type,
                         FieldType.INSTANCE)
        self.assertEqual(profile_field.definition.field_storage,
                         FieldStorage.FOREIGN_KEY)
        self.assertEqual(profile_field.definition.foreign_key, 'user')
        self.assertEqual(profile_field.definition.use_join_table, False)

        user_field = LinkedProfile.definition.field_named('user')
        self.assertEqual(user_field.definition.field_type,
                         FieldType.INSTANCE)
        self.assertEqual(user_field.definition.field_storage,
                         FieldStorage.LOCAL_KEY)
        self.assertEqual(user_field.definition.foreign_key, None)
        self.assertEqual(user_field.definition.use_join_table, None)

    def test_auto_generates_1_to_many_links(self):
        articles_field = LinkedAuthor.definition.field_named('articles')
        self.assertEqual(articles_field.definition.field_type,
                         FieldType.LIST)
        self.assertEqual(articles_field.definition.field_storage,
                         FieldStorage.FOREIGN_KEY)
        self.assertEqual(articles_field.definition.foreign_key, 'author')
        self.assertEqual(articles_field.definition.use_join_table, False)

        author_field = LinkedArticle.definition.field_named('author')
        self.assertEqual(author_field.definition.field_type,
                         FieldType.INSTANCE)
        self.assertEqual(author_field.definition.field_storage,
                         FieldStorage.LOCAL_KEY)
        self.assertEqual(author_field.definition.foreign_key, None)
        self.assertEqual(author_field.definition.use_join_table, None)

    def test_auto_generates_many_to_many_links(self):
        customer1 = LinkedCustomer(name='C1')
        customer2 = LinkedCustomer(name='C2')
        product1 = LinkedProduct(name='P1')
        product2 = LinkedProduct(name='P2')
        customer1.products.append(product1)
        customer1.products.append(product2)
        product1.customers.append(customer2)
        self.assertEqual(customer1.products, [product1, product2])
        self.assertEqual(product1.customers, [customer1, customer2])
        self.assertEqual(customer2.products, [product1])
        self.assertEqual(product2.customers, [customer1])
