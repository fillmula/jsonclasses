import unittest
from typing import Optional, List, Dict
from jsonclasses import jsonclass, JSONObject, ValidationException
from datetime import datetime, date


class TestJSONObjectAutoTypesMarkersGeneration(unittest.TestCase):

    def test_auto_generates_required_str(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestStr(JSONObject):
            val: str
        object = TestStr()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_str(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionalStr(JSONObject):
            val: Optional[str]
        object = TestOptionalStr()
        object.validate()

    def test_auto_generates_required_str_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestStrStrType(JSONObject):
            val: 'str'
        object = TestStrStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_str_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionalStrStrType(JSONObject):
            val: 'Optional[str]'
        object = TestOptionalStrStrType()
        object.validate()

    def test_auto_generates_required_int(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestInt(JSONObject):
            val: int
        object = TestInt()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_int(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionalInt(JSONObject):
            val: Optional[int]
        object = TestOptionalInt()
        object.validate()

    def test_auto_generates_required_int_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestIntStrType(JSONObject):
            val: 'int'
        object = TestIntStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_int_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionalIntStrType(JSONObject):
            val: 'Optional[int]'
        object = TestOptionalIntStrType()
        object.validate()

    def test_auto_generates_required_float(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestFloat(JSONObject):
            val: float
        object = TestFloat()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_float(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionalfloat(JSONObject):
            val: Optional[float]
        object = TestOptionalfloat()
        object.validate()

    def test_auto_generates_required_float_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestFloatStrType(JSONObject):
            val: 'float'
        object = TestFloatStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_float_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionalFloatStrType(JSONObject):
            val: 'Optional[float]'
        object = TestOptionalFloatStrType()
        object.validate()

    def test_auto_generates_required_bool(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestBool(JSONObject):
            val: bool
        object = TestBool()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_bool(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionalbool(JSONObject):
            val: Optional[bool]
        object = TestOptionalbool()
        object.validate()

    def test_auto_generates_required_bool_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestboolStrType(JSONObject):
            val: 'bool'
        object = TestboolStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_bool_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionalboolStrType(JSONObject):
            val: 'Optional[bool]'
        object = TestOptionalboolStrType()
        object.validate()

    def test_auto_generates_required_date(self):
        @jsonclass(graph='test_marker_auto_gen')
        class Testdate(JSONObject):
            val: date
        object = Testdate()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_date(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionaldate(JSONObject):
            val: Optional[date]
        object = TestOptionaldate()
        object.validate()

    def test_auto_generates_required_date_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestdateStrType(JSONObject):
            val: 'date'
        object = TestdateStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_date_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionaldateStrType(JSONObject):
            val: 'Optional[date]'
        object = TestOptionaldateStrType()
        object.validate()

    def test_auto_generates_required_datetime(self):
        @jsonclass(graph='test_marker_auto_gen')
        class Testdatetime(JSONObject):
            val: datetime
        object = Testdatetime()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_datetime(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionaldatetime(JSONObject):
            val: Optional[datetime]
        object = TestOptionaldatetime()
        object.validate()

    def test_auto_generates_required_datetime_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestdatetimeStrType(JSONObject):
            val: 'datetime'
        object = TestdatetimeStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_datetime_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionaldatetimeStrType(JSONObject):
            val: 'Optional[datetime]'
        object = TestOptionaldatetimeStrType()
        object.validate()

    def test_auto_generates_required_list(self):
        @jsonclass(graph='test_marker_auto_gen')
        class Testlist(JSONObject):
            val: List[str]
        object = Testlist()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_list(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionallist(JSONObject):
            val: Optional[List[str]]
        object = TestOptionallist()
        object.validate()

    def test_auto_generates_required_list_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestlistStrType(JSONObject):
            val: 'List[str]'
        object = TestlistStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_list_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionallistStrType(JSONObject):
            val: 'Optional[List[str]]'
        object = TestOptionallistStrType()
        object.validate()

    def test_auto_generates_required_dict(self):
        @jsonclass(graph='test_marker_auto_gen')
        class Testdict(JSONObject):
            val: Dict[str, str]
        object = Testdict()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_dict(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionaldict(JSONObject):
            val: Optional[Dict[str, str]]
        object = TestOptionaldict()
        object.validate()

    def test_auto_generates_required_dict_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestdictStrType(JSONObject):
            val: 'Dict[str, str]'
        object = TestdictStrType()
        self.assertRaises(ValidationException, object.validate)

    def test_auto_generates_optional_dict_with_str_type(self):
        @jsonclass(graph='test_marker_auto_gen')
        class TestOptionaldictStrType(JSONObject):
            val: 'Optional[Dict[str, str]]'
        object = TestOptionaldictStrType()
        object.validate()
