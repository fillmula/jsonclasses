from jsonclasses.fields import FieldType, field
from unittest import TestCase
from typing import Optional, List, Dict, Union
from jsonclasses import jsonclass, JSONObject, ValidationException
from datetime import datetime, date


class TestJSONObjectTypesSynthesis(TestCase):

    def test_auto_generates_required_str(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestStr(JSONObject):
            val: str
        object = TestStr()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_str(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalStr(JSONObject):
            val: Optional[str]
        object = TestOptionalStr()
        object.validate()

    def test_auto_generates_required_str_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestStrStrType(JSONObject):
            val: 'str'
        object = TestStrStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_str_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalStrStrType(JSONObject):
            val: 'Optional[str]'
        object = TestOptionalStrStrType()
        object.validate()

    def test_auto_generates_required_int(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestInt(JSONObject):
            val: int
        object = TestInt()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_int(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalInt(JSONObject):
            val: Optional[int]
        object = TestOptionalInt()
        object.validate()

    def test_auto_generates_required_int_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestIntStrType(JSONObject):
            val: 'int'
        object = TestIntStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_int_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalIntStrType(JSONObject):
            val: 'Optional[int]'
        object = TestOptionalIntStrType()
        object.validate()

    def test_auto_generates_required_float(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestFloat(JSONObject):
            val: float
        object = TestFloat()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_float(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalfloat(JSONObject):
            val: Optional[float]
        object = TestOptionalfloat()
        object.validate()

    def test_auto_generates_required_float_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestFloatStrType(JSONObject):
            val: 'float'
        object = TestFloatStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_float_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalFloatStrType(JSONObject):
            val: 'Optional[float]'
        object = TestOptionalFloatStrType()
        object.validate()

    def test_auto_generates_required_bool(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestBool(JSONObject):
            val: bool
        object = TestBool()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_bool(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalbool(JSONObject):
            val: Optional[bool]
        object = TestOptionalbool()
        object.validate()

    def test_auto_generates_required_bool_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestboolStrType(JSONObject):
            val: 'bool'
        object = TestboolStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_bool_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalboolStrType(JSONObject):
            val: 'Optional[bool]'
        object = TestOptionalboolStrType()
        object.validate()

    def test_auto_generates_required_date(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class Testdate(JSONObject):
            val: date
        object = Testdate()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_date(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionaldate(JSONObject):
            val: Optional[date]
        object = TestOptionaldate()
        object.validate()

    def test_auto_generates_required_date_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestdateStrType(JSONObject):
            val: 'date'
        object = TestdateStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_date_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionaldateStrType(JSONObject):
            val: 'Optional[date]'
        object = TestOptionaldateStrType()
        object.validate()

    def test_auto_generates_required_datetime(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class Testdatetime(JSONObject):
            val: datetime
        object = Testdatetime()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_datetime(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionaldatetime(JSONObject):
            val: Optional[datetime]
        object = TestOptionaldatetime()
        object.validate()

    def test_auto_generates_required_datetime_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestdatetimeStrType(JSONObject):
            val: 'datetime'
        object = TestdatetimeStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_datetime_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionaldatetimeStrType(JSONObject):
            val: 'Optional[datetime]'
        object = TestOptionaldatetimeStrType()
        object.validate()

    def test_auto_generates_required_list(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class Testlist(JSONObject):
            val: list[str]
        object = Testlist()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_list(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class TestOptionallist(JSONObject):
            val: Optional[list[str]]
        object = TestOptionallist()
        object.validate()

    def test_auto_generates_required_list_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class TestlistStrType(JSONObject):
            val: 'list[str]'
        object = TestlistStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_list_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class TestOptionallistStrType(JSONObject):
            val: 'Optional[list[str]]'
        object = TestOptionallistStrType()
        object.validate()

    def test_auto_generates_required_list_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class Testlist(JSONObject):
            val: List[str]
        object = Testlist()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_list_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionallist(JSONObject):
            val: Optional[List[str]]
        object = TestOptionallist()
        object.validate()

    def test_auto_generates_required_list_with_str_type_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestlistStrType(JSONObject):
            val: 'List[str]'
        object = TestlistStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_list_with_str_type_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionallistStrType(JSONObject):
            val: 'Optional[List[str]]'
        object = TestOptionallistStrType()
        object.validate()

    def test_auto_generates_required_dict(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class Testdict(JSONObject):
            val: dict[str, str]
        object = Testdict()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_dict(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class TestOptionaldict(JSONObject):
            val: Optional[dict[str, str]]
        object = TestOptionaldict()
        object.validate()

    def test_auto_generates_required_dict_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class TestdictStrType(JSONObject):
            val: 'dict[str, str]'
        object = TestdictStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_dict_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen_2')
        class TestOptionaldictStrType(JSONObject):
            val: 'Optional[dict[str, str]]'
        object = TestOptionaldictStrType()
        object.validate()

    def test_auto_generates_required_dict_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class Testdict(JSONObject):
            val: Dict[str, str]
        object = Testdict()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_dict_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionaldict(JSONObject):
            val: Optional[Dict[str, str]]
        object = TestOptionaldict()
        object.validate()

    def test_auto_generates_required_dict_with_str_type_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestdictStrType(JSONObject):
            val: 'Dict[str, str]'
        object = TestdictStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_dict_with_str_type_capitalized(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionaldictStrType(JSONObject):
            val: 'Optional[Dict[str, str]]'
        object = TestOptionaldictStrType()
        object.validate()

    def test_auto_generates_required_instance(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestinstanceReferenced(JSONObject):
            val: Optional[str]

        @jsonclass(class_graph='test_marker_auto_gen')
        class Testinstance(JSONObject):
            val: TestinstanceReferenced
        object = Testinstance()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_instance(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestoptionalinstanceReferenced(JSONObject):
            val: Optional[str]

        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalInstance(JSONObject):
            val: Optional[TestoptionalinstanceReferenced]
        object = TestOptionalInstance()
        object.validate()

    def test_auto_generates_required_instance_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestinstanceReferencedWithStrType(JSONObject):
            val: Optional[str]

        @jsonclass(class_graph='test_marker_auto_gen')
        class TestinstanceWithStrType(JSONObject):
            val: 'TestinstanceReferencedWithStrType'
        object = TestinstanceWithStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_instance_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestoptionalinstanceReferencedWithStrType(JSONObject):
            val: Optional[str]

        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalInstanceWithStrType(JSONObject):
            val: 'Optional[TestoptionalinstanceReferencedWithStrType]'
        object = TestOptionalInstanceWithStrType()
        object.validate()

    def test_auto_generates_required_union(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestUnion(JSONObject):
            val: Union[str, bool]
        object = TestUnion()
        self.assertFalse(object.is_valid())

    def test_auto_generates_optional_union(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalUnion(JSONObject):
            val: Optional[Union[str, bool]]
        object = TestOptionalUnion()
        object.validate()

    def test_auto_generates_required_union_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestUnionStrType(JSONObject):
            val: 'Union[str, int]'
        object = TestUnionStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_union_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalUnionStrType(JSONObject):
            val: 'Optional[Union[int, float]]'
        object = TestOptionalUnionStrType()
        object.validate()

    def test_auto_generates_required_union_with_dict_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestUnionDictType(JSONObject):
            val: 'Union[Dict[str, int], int]'
        cfield = field(TestUnionDictType, 'val')
        utypes = cfield.fdesc.union_types
        self.assertEqual(utypes[0].fdesc.field_type, FieldType.DICT)
        self.assertEqual(utypes[1].fdesc.field_type, FieldType.INT)

    def test_auto_generates_optional_union_with_dict_with_str_type(self):
        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOptionalUnionDictType(JSONObject):
            val: 'Optional[Union[Dict[str, bool], float]]'
        object = TestOptionalUnionDictType()
        object.validate()
