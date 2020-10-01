from __future__ import annotations
import unittest
from typing import List, Dict
from jsonclasses import jsonclass, JSONObject, types
from jsonclasses.exceptions import ValidationException


class TestInstanceOfValidator(unittest.TestCase):

    def test_instanceof_validator_creates_instanceof_designated_class_on_transforming(self):
        @jsonclass(graph='test_instanceof_1')
        class Address(JSONObject):
            line1: str = types.str
            line2: str = types.str

        @jsonclass(graph='test_instanceof_1')
        class User(JSONObject):
            name: str = types.str
            address: Address = types.instanceof(Address)
        user = User(**{'name': 'John', 'address': {'line1': 'London', 'line2': 'Road'}})
        self.assertIsInstance(user.address, Address)

    def test_instanceof_validator_validates_using_validator_inside(self):
        @jsonclass(graph='test_instanceof_2')
        class Address(JSONObject):
            line1: str = types.str.required
            line2: str = types.str

        @jsonclass(graph='test_instanceof_2')
        class User(JSONObject):
            name: str = types.str
            address: Address = types.instanceof(Address)
        user = User(**{'name': 'John', 'address': {'line2': 'Road'}})
        self.assertRaisesRegex(ValidationException, 'Value at \'address\\.line1\' should not be None.', user.validate)

    def test_instanceof_validator_convert_subfields_to_json(self):
        @jsonclass(graph='test_instanceof_3')
        class Address(JSONObject):
            line1: str = types.str.required
            line2: str = types.str

        @jsonclass(graph='test_instanceof_3')
        class User(JSONObject):
            name: str = types.str
            address: Address = types.instanceof(Address)
        user = User(**{'name': 'John', 'address': {'line2': 'Road', 'line1': 'OK'}})
        result = user.tojson()
        self.assertEqual(result, {'name': 'John', 'address': {'line1': 'OK', 'line2': 'Road'}})

    def test_instanceof_validator_creates_instances_inside_list(self):
        @jsonclass(graph='test_instanceof_4')
        class Address(JSONObject):
            line1: str = types.str
            line2: str = types.str

        @jsonclass(graph='test_instanceof_4')
        class User(JSONObject):
            name: str = types.str
            addresses: List[Address] = types.listof(types.instanceof(Address))
        user = User(**{'name': 'John', 'addresses': [
            {'line1': 'London', 'line2': 'Road'},
            {'line1': 'Paris', 'line2': 'Road'},
        ]})
        self.assertIsInstance(user.addresses[0], Address)
        self.assertIsInstance(user.addresses[1], Address)
        self.assertEqual(len(user.addresses), 2)
        self.assertEqual(user.addresses[0].__dict__, {'line1': 'London', 'line2': 'Road'})
        self.assertEqual(user.addresses[1].__dict__, {'line1': 'Paris', 'line2': 'Road'})

    def test_instanceof_validator_validates_instances_inside_list(self):
        @jsonclass(graph='test_instanceof_5')
        class Address(JSONObject):
            line1: str = types.str.required
            line2: str = types.str.required

        @jsonclass(graph='test_instanceof_5')
        class User(JSONObject):
            name: str = types.str
            addresses: List[Address] = types.listof(types.instanceof(Address))
        user = User(**{'name': 'John', 'addresses': [
            {'line1': 'London'},
            {'line1': 'Paris'},
        ]})
        self.assertRaises(ValidationException, user.validate)

    def test_instanceof_validator_converts_to_json_inside_list(self):
        @jsonclass(graph='test_instanceof_6')
        class Address(JSONObject):
            line1: str = types.str
            line2: str = types.str

        @jsonclass(graph='test_instanceof_6')
        class User(JSONObject):
            name: str = types.str
            addresses: List[Address] = types.listof(types.instanceof(Address))
        user = User(**{'name': 'John', 'addresses': [
            {'line1': 'London', 'line2': 'Road'},
            {'line1': 'Paris', 'line2': 'Road'},
        ]})
        result = user.tojson()
        desired = {'name': 'John', 'addresses': [{'line1': 'London', 'line2': 'Road'}, {'line1': 'Paris', 'line2': 'Road'}]}
        self.assertEqual(result, desired)

    def test_instanceof_validator_allow_argument_to_be_string(self):
        @jsonclass(graph='test_instanceof_7')
        class Post(JSONObject):
            title: str = types.str
            content: str = types.str
            author: User = types.instanceof('User')

        @jsonclass(graph='test_instanceof_7')
        class User(JSONObject):
            name: str = types.str
            posts: List[Post] = types.listof(types.instanceof('Post'))
        user = User(**{'name': 'John', 'posts': [
            {'title': 'P1', 'content': 'C1'},
            {'title': 'P2', 'content': 'C2'},
        ]})
        self.assertIs(user.posts[0].__class__, Post)
        self.assertIs(user.posts[1].__class__, Post)
        result = user.tojson()
        desired = {
            'name': 'John',
            'posts': [
                {'title': 'P1', 'content': 'C1', 'author': None},
                {'title': 'P2', 'content': 'C2', 'author': None}
            ]
        }
        self.assertEqual(result, desired)

    def test_instanceof_works_without_assigning_a_types(self):
        @jsonclass(graph='test_instanceof_8')
        class Staff(JSONObject):
            position: str
            user: User

        @jsonclass(graph='test_instanceof_8')
        class User(JSONObject):
            name: str = types.str
            staff: Staff
        user = User(**{'name': 'John', 'staff': {'position': 'CEO'}})
        self.assertIsInstance(user.staff, Staff)
        self.assertEqual(user.staff.position, 'CEO')
        staff = Staff(**{'position': 'Developer', 'user': {'name': 'Valy'}})
        self.assertIsInstance(staff.user, User)
        self.assertEqual(staff.user.name, 'Valy')

    def test_instanceof_works_in_list_without_assigning_a_types(self):
        @jsonclass(graph='test_instanceof_9')
        class Staff(JSONObject):
            position: str
            users: List[User]

        @jsonclass(graph='test_instanceof_9')
        class User(JSONObject):
            name: str
            staffs: List[Staff]
        user = User(**{'name': 'John', 'staffs': [{'position': 'CEO'}, {'position': 'CSO'}]})
        self.assertIsInstance(user.staffs[0], Staff)
        self.assertEqual(user.staffs[0].position, 'CEO')
        staff = Staff(**{'position': 'Developer', 'users': [{'name': 'Valy'}, {'name': 'Jonny'}]})
        self.assertIsInstance(staff.users[0], User)
        self.assertEqual(staff.users[0].name, 'Valy')

    def test_instanceof_works_in_dict_without_assigning_a_types(self):
        @jsonclass(graph='test_instanceof_10')
        class Staff(JSONObject):
            position: str
            users: Dict[str, User]

        @jsonclass(graph='test_instanceof_10')
        class User(JSONObject):
            name: str
            staffs: Dict[str, Staff]
        user = User(**{'name': 'John', 'staffs': {'a': {'position': 'CEO'}, 'b': {'position': 'CSO'}}})
        self.assertIsInstance(user.staffs['a'], Staff)
        self.assertEqual(user.staffs['a'].position, 'CEO')
        staff = Staff(**{'position': 'Developer', 'users': {'a': {'name': 'Valy'}, 'b': {'name': 'Jonny'}}})
        self.assertIsInstance(staff.users['a'], User)
        self.assertEqual(staff.users['a'].name, 'Valy')

    def test_instanceof_validates_in_list_without_assigning_a_types(self):
        @jsonclass(graph='test_instanceof_11')
        class Staff(JSONObject):
            position: str
            users: List[User]

        @jsonclass(graph='test_instanceof_11')
        class User(JSONObject):
            name: str
            staffs: List[Staff]
        user = User(**{'name': 'John', 'staffs': [{'position': 'CEO'}, None, {'position': 'CSO'}]})
        with self.assertRaisesRegex(ValidationException, 'Value at \'staffs\\.1\' should not be None\\.'):
            user.validate()

    def test_instanceof_validates_in_dict_without_assigning_a_types(self):
        @jsonclass(graph='test_instanceof_12')
        class Staff(JSONObject):
            position: str
            users: Dict[str, User]

        @jsonclass(graph='test_instanceof_12')
        class User(JSONObject):
            name: str
            staffs: Dict[str, Staff]
        user = User(**{'name': 'John', 'staffs': {'a': {'position': 'CEO'}, 'b': None, 'c': {'position': 'CSO'}}})
        with self.assertRaisesRegex(ValidationException, 'Value at \'staffs\\.b\' should not be None\\.'):
            user.validate()

    def test_instanceof_raises_if_strict_specified(self):
        @jsonclass(graph='test_instanceof_13')
        class Staff(JSONObject):
            position: str
            user: User = types.instanceof('User').required

        @jsonclass(graph='test_instanceof_13')
        class User(JSONObject):
            name: str
            staff: Staff = types.instanceof('Staff').strict.required
        with self.assertRaisesRegex(ValidationException, "Key 'boom' at 'staff' is now allowed\\."):
            User(**{'name': 'John', 'staff': {'position': 'CEO', 'boom': True}})

    def test_instanceof_raises_if_strict_instance(self):
        @jsonclass(graph='test_instanceof_14', strict_input=True)
        class Staff(JSONObject):
            position: str
            user: User = types.instanceof('User').required

        @jsonclass(graph='test_instanceof_14')
        class User(JSONObject):
            name: str
            staff: Staff = types.instanceof('Staff').required
        with self.assertRaisesRegex(ValidationException, "Key 'boom' at 'staff' is now allowed\\."):
            User(**{'name': 'John', 'staff': {'position': 'CEO', 'boom': True}})

    def test_instanceof_create_circular_ref_for_local_and_foreign_binding(self):

        @jsonclass(graph='test_instanceof_15')
        class Staff(JSONObject):
            position: str
            user: User = types.linkto.instanceof('User').required

        @jsonclass(graph='test_instanceof_15')
        class User(JSONObject):
            name: str
            staff: Staff = types.instanceof('Staff').linkedby('user').required

        user = User(**{'name': 'John', 'staff': {'position': 'CEO'}})
        self.assertEqual(user.staff.user, user)

    def test_instanceof_create_circular_ref_for_foreign_and_local_binding(self):

        @jsonclass(graph='test_instanceof_16')
        class Staff(JSONObject):
            position: str
            user: User = types.instanceof('User').linkedby('staff').required

        @jsonclass(graph='test_instanceof_16')
        class User(JSONObject):
            name: str
            staff: Staff = types.linkto.instanceof('Staff').required

        user = User(**{'name': 'John', 'staff': {'position': 'CEO'}})
        self.assertEqual(user.staff.user, user)

    def test_instanceof_create_circular_ref_for_foreign_list_and_local_binding(self):

        @jsonclass(graph='test_instanceof_17')
        class Post(JSONObject):
            title: str
            user: User = types.linkto.instanceof('User').required

        @jsonclass(graph='test_instanceof_17')
        class User(JSONObject):
            name: str
            posts: List[Post] = types.listof('Post').linkedby('user').required

        user = User(**{'name': 'John', 'posts': [{'title': 'A'}, {'title': 'B'}]})
        self.assertEqual(user.posts[0].user, user)
        self.assertEqual(user.posts[1].user, user)

    def test_instanceof_create_circular_ref_for_local_list_and_foreign_binding(self):

        @jsonclass(graph='test_instanceof_18')
        class Post(JSONObject):
            title: str
            user: User = types.instanceof('User').linkedby('posts').required

        @jsonclass(graph='test_instanceof_18')
        class User(JSONObject):
            name: str
            posts: List[Post] = types.linkto.listof('Post').required

        user = User(**{'name': 'John', 'posts': [{'title': 'A'}, {'title': 'B'}]})
        self.assertEqual(user.posts[0].user, user)
        self.assertEqual(user.posts[1].user, user)

    def test_instanceof_create_circular_ref_for_foreign_item_and_local_list_binding(self):

        @jsonclass(graph='test_instanceof_19')
        class Post(JSONObject):
            title: str
            user: User = types.linkto.instanceof('User').required

        @jsonclass(graph='test_instanceof_19')
        class User(JSONObject):
            name: str
            posts: List[Post] = types.listof('Post').linkedby('user').required
        post = Post(**{'title': 'A', 'user': {'name': 'B'}})
        self.assertEqual(post.user.posts[0], post)

    def test_instanceof_create_circular_ref_for_local_list_and_foreign_item_binding(self):

        @jsonclass(graph='test_instanceof_20')
        class Post(JSONObject):
            title: str
            user: User = types.instanceof('User').linkedby('posts').required

        @jsonclass(graph='test_instanceof_20')
        class User(JSONObject):
            name: str
            posts: List[Post] = types.linkto.listof('Post').required

        post = Post(**{'title': 'A', 'user': {'name': 'B'}})
        self.assertEqual(post.user.posts[0], post)

    def test_instanceof_create_circular_ref_for_many_to_many(self):

        @jsonclass(graph='test_instanceof_21')
        class Book(JSONObject):
            title: str
            users: List[User] = types.listof('User').linkedthru('books').required

        @jsonclass(graph='test_instanceof_21')
        class User(JSONObject):
            name: str
            books: List[Book] = types.listof('Book').linkedthru('users').required

        book = Book(**{'title': 'A', 'users': [{'name': 'A'}, {'name': 'B'}]})
        self.assertEqual(book.users[0].books[0], book)
        self.assertEqual(book.users[1].books[0], book)

    def test_instance_of_accepts_object(self):

        @jsonclass(graph='test_instanceof_22')
        class Staff(JSONObject):
            position: str
            user: User = types.linkto.instanceof('User').required

        @jsonclass(graph='test_instanceof_22')
        class User(JSONObject):
            name: str
            staff: Staff = types.instanceof('Staff').linkedby('user').required

        staff = Staff(position='CFO')
        user = User(name='John', staff=staff)
        self.assertEqual(user.staff.user, user)
