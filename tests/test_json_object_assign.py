from __future__ import annotations
from unittest import TestCase
from jsonclasses import jsonclass, JSONObject, types


@jsonclass(graph='test_json_object_assign')
class Staff(JSONObject):
    id: int
    position: str
    user: User = types.linkto.instanceof('User').required


@jsonclass(graph='test_json_object_assign')
class User(JSONObject):
    id: int
    name: str
    staff: Staff = types.instanceof('Staff').linkedby('user').required


class TestJSONObjectAssign(TestCase):

    def test_json_objects_connects_thru_assign(self):
        staff = Staff(id=1, position='CEO')
        user = User(id=1, name='Victor')
        user.staff = staff
        self.assertEqual(user.staff.user, user)
        self.assertEqual(staff.user.staff, staff)
