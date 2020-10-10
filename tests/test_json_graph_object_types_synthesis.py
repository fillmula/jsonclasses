from __future__ import annotations
from typing import cast
from jsonclasses.fields import FieldType, FieldStorage, field
from unittest import TestCase
from jsonclasses import (jsonclass, JSONObject, Types,
                         Link, linkto, linkedby, linkedthru)


class TestJSONObjectTypesSynthesis(TestCase):

    def test_auto_generates_1_1_local_key_foreign_key(self):

        @jsonclass(class_graph='test_marker_auto_gen')
        class TestLocalKeyOne(JSONObject):
            name: str
            two: Link[TestLocalKeyTwo, linkedby('one')]

        @jsonclass(class_graph='test_marker_auto_gen')
        class TestLocalKeyTwo(JSONObject):
            name: str
            one: Link[TestLocalKeyOne, linkto]

        ones_field_two = field(TestLocalKeyOne, 'two')
        self.assertEqual(ones_field_two.field_description.field_type,
                         FieldType.INSTANCE)
        self.assertEqual(ones_field_two.field_description.field_storage,
                         FieldStorage.FOREIGN_KEY)
        self.assertEqual(ones_field_two.field_description.foreign_key, 'one')
        self.assertEqual(ones_field_two.field_description.use_join_table,
                         False)

        twos_field_one = field(TestLocalKeyTwo, 'one')
        self.assertEqual(twos_field_one.field_description.field_type,
                         FieldType.INSTANCE)
        self.assertEqual(twos_field_one.field_description.field_storage,
                         FieldStorage.LOCAL_KEY)
        self.assertEqual(twos_field_one.field_description.foreign_key, None)
        self.assertEqual(twos_field_one.field_description.use_join_table,
                         None)

    def test_auto_generates_1_many_local_key_foreign_key(self):

        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOMKeyOne(JSONObject):
            name: str
            master: Link[TestOMKeyMany, linkto]

        @jsonclass(class_graph='test_marker_auto_gen')
        class TestOMKeyMany(JSONObject):
            name: str
            slaves: Link[list[TestOMKeyOne], linkedby('master')]

        master_field = field(TestOMKeyOne, 'master')
        self.assertEqual(master_field.field_description.field_type,
                         FieldType.INSTANCE)
        self.assertEqual(master_field.field_description.field_storage,
                         FieldStorage.LOCAL_KEY)
        self.assertEqual(master_field.field_description.foreign_key, None)

        slave_fields = field(TestOMKeyMany, 'slaves')
        self.assertEqual(slave_fields.field_description.field_type,
                         FieldType.LIST)
        self.assertEqual(slave_fields.field_description.field_storage,
                         FieldStorage.FOREIGN_KEY)
        self.assertEqual(slave_fields.field_description.foreign_key, 'master')

    def test_auto_generates_many_many_foreign_key(self):

        @jsonclass(class_graph='test_marker_auto_gen_q')
        class TestManyManyKeyTwo(JSONObject):
            name: str
            ones: Link[list[TestManyManyKeyOne], linkedthru('twos')]

        @jsonclass(class_graph='test_marker_auto_gen_q')
        class TestManyManyKeyOne(JSONObject):
            name: str
            twos: Link[list[TestManyManyKeyTwo], linkedthru('ones')]

        twos_field_ones = field(TestManyManyKeyTwo, 'ones')
        self.assertEqual(twos_field_ones.field_description.field_type,
                         FieldType.LIST)
        ones_item_types = cast(Types,
                               twos_field_ones.field_description.list_item_types)
        self.assertEqual(ones_item_types.field_description.instance_types,
                         TestManyManyKeyOne)

        ones_field_twos = field(TestManyManyKeyOne, 'twos')
        self.assertEqual(ones_field_twos.field_description.field_type,
                         FieldType.LIST)
        twos_item_types = cast(Types,
                               ones_field_twos.field_description.list_item_types)
        self.assertEqual(twos_item_types.field_description.instance_types,
                         TestManyManyKeyTwo)

        self.assertEqual(twos_field_ones.field_description.field_storage,
                         FieldStorage.FOREIGN_KEY)
        self.assertEqual(twos_field_ones.field_description.foreign_key, 'twos')
        self.assertEqual(twos_field_ones.field_description.use_join_table,
                         True)

        self.assertEqual(ones_field_twos.field_description.field_storage,
                         FieldStorage.FOREIGN_KEY)
        self.assertEqual(ones_field_twos.field_description.foreign_key, 'ones')
        self.assertEqual(ones_field_twos.field_description.use_join_table,
                         True)
