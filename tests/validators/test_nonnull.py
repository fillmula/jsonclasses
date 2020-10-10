from unittest import TestCase
from typing import Annotated, Optional, TypedDict
from jsonclasses import jsonclass, JSONObject, types, linkedby


class TestNonnullValidator(TestCase):

    def test_nonnull_ref_list_has_default_value_empty_array(self):
        @jsonclass(class_graph='test_nonnull_1')
        class Item(JSONObject):
            box: 'Annotated[Box, linkto]'

        @jsonclass(class_graph='test_nonnull_1')
        class Box(JSONObject):
            items: Annotated[list[Item], linkedby('box')]

        box = Box()
        self.assertEqual(box.items, [])

    def test_nonnull_list_has_default_value_empty_array(self):

        @jsonclass(class_graph='test_nonnull_2')
        class Box(JSONObject):
            items: list[str] = types.nonnull.listof(str)

        box = Box()
        self.assertEqual(box.items, [])

    def test_nonnull_dict_has_default_value_empty_dict(self):

        @jsonclass(class_graph='test_nonnull_3')
        class Box(JSONObject):
            items: dict[str, str] = types.nonnull.dictof(str)

        box = Box()
        self.assertEqual(box.items, {})

    def test_nonnull_shape_has_default_value_empty_dict(self):

        class Items(TypedDict):
            item_a: Optional[str]
            item_b: Optional[int]

        @jsonclass(class_graph='test_nonnull_4')
        class Box(JSONObject):
            items: Items = types.nonnull.shape({
                'item_a': types.str.required,
                'item_b': types.int.required
            })

        box = Box()
        self.assertEqual(box.items, {'item_a': None, 'item_b': None})
