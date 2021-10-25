from __future__ import annotations
from unittest import TestCase
from typing import List, Dict, Optional
from jsonclasses import jsonclass, types
from jsonclasses.excs import ValidationException


@jsonclass(class_graph='test_instanceof_22')
class User:
    id: int = types.int.primary
    name: str
    posts: List[Post] = types.listof('Post').linkedby('user').required
    comments: List[Comment] = types.listof('Comment').linkedby('commenter').required


@jsonclass(class_graph='test_instanceof_22')
class Post:
    id: int = types.int.primary
    name: str
    user: User = types.linkto.objof('User').required
    comments: List[Comment] = types.listof('Comment').linkedby('post').required


@jsonclass(class_graph='test_instanceof_22')
class Comment:
    id: int = types.int.primary
    content: str
    post: Post = types.linkto.objof('Post').required
    parent: Optional[Comment] = types.linkto.objof('Comment')
    children: List[Comment] = types.listof('Comment').linkedby('parent').required
    commenter: User = types.linkto.objof('User').required


input = {
    'id': 1,
    'name': 'U1',
    'posts': [
        {
            'id': 1,
            'name': 'P1',
            'comments': [
                {
                    'id': 1,
                    'content': 'C1',
                    'commenter': {
                        'id': 2,
                        'name': 'U2'
                    }
                },
                {
                    'id': 2,
                    'content': 'C2',
                    'parent': {
                        'id': 1,
                        'content': 'C1'
                    },
                    'commenter': {
                        'id': 1,
                        'name': 'U1'
                    }
                },
                {
                    'id': 3,
                    'content': 'C3',
                    'commenter': {
                        'id': 2,
                        'name': 'U2'
                    }
                }
            ]
        },
        {
            'id': 2,
            'name': 'P2',
            'comments': [
                {
                    'id': 4,
                    'content': 'C4',
                    'commenter': {
                        'id': 2,
                        'name': 'U2'
                    }
                },
                {
                    'id': 5,
                    'content': 'C5',
                    'commenter': {
                        'id': 3,
                        'name': 'U3'
                    }
                }
            ]
        }
    ]
}


class TestInstanceOfModifier(TestCase):

    def test_instanceof_modifier_creates_instanceof_designated_class_on_transforming(self):
        @jsonclass(class_graph='test_instanceof_1')
        class Address:
            line1: str = types.str
            line2: str = types.str

        @jsonclass(class_graph='test_instanceof_1')
        class User:
            name: str = types.str
            address: Address = types.objof(Address)
        user = User(**{'name': 'John', 'address': {'line1': 'London', 'line2': 'Road'}})
        self.assertIsInstance(user.address, Address)

    def test_instanceof_modifier_fill_children_defaults(self):
        @jsonclass(class_graph='test_instanceof_1_0')
        class Address:
            line1: str = types.str.default('Line1').required
            line2: str = types.str.default('Line2').required

        @jsonclass(class_graph='test_instanceof_1_0')
        class User:
            name: str = types.str.required
            address: Address = types.objof(Address).required
        user = User(**{'name': 'John', 'address': {}})
        self.assertEqual(user.address.line1, 'Line1')
        self.assertEqual(user.address.line2, 'Line2')

    def test_instanceof_modifier_raises_if_type_doesnt_match(self):
        @jsonclass(class_graph='test_instanceof_1_2')
        class Address:
            line1: str = types.str.required
            line2: str = types.str.required

        @jsonclass(class_graph='test_instanceof_1_2')
        class NewAddress:
            line3: str = types.str.required
            line4: str = types.str.required

        @jsonclass(class_graph='test_instanceof_1_2')
        class User:
            name: str = types.str.required
            address: Address = types.objof(Address).required
        user = User(name='John')
        user.address = NewAddress(line3='1', line4='2')
        self.assertRaisesRegex(
            ValidationException,
            "value is not instance of Address",
            user.validate)

    def test_instanceof_modifier_validates_using_modifier_inside(self):
        @jsonclass(class_graph='test_instanceof_2')
        class Address:
            line1: str = types.str.required
            line2: str = types.str

        @jsonclass(class_graph='test_instanceof_2')
        class User:
            name: str = types.str
            address: Address = types.objof(Address)
        user = User(**{'name': 'John', 'address': {'line2': 'Road'}})
        self.assertRaisesRegex(ValidationException,
            "'address\\.line1': value required",
            user.validate)

    def test_instanceof_modifier_convert_subfields_to_json(self):
        @jsonclass(class_graph='test_instanceof_3')
        class Address:
            line1: str = types.str.required
            line2: str = types.str

        @jsonclass(class_graph='test_instanceof_3')
        class User:
            name: str = types.str
            address: Address = types.objof(Address)
        user = User(**{'name': 'John', 'address': {'line2': 'Road', 'line1': 'OK'}})
        result = user.tojson()
        self.assertEqual(result, {'name': 'John', 'address': {'line1': 'OK', 'line2': 'Road'}})

    def test_instanceof_modifier_creates_instances_inside_list(self):
        @jsonclass(class_graph='test_instanceof_4')
        class Address:
            line1: str = types.str
            line2: str = types.str

        @jsonclass(class_graph='test_instanceof_4')
        class User:
            name: str = types.str
            addresses: List[Address] = types.listof(types.objof(Address))
        user = User(**{'name': 'John', 'addresses': [
            {'line1': 'London', 'line2': 'Road'},
            {'line1': 'Paris', 'line2': 'Road'},
        ]})
        self.assertIsInstance(user.addresses[0], Address)
        self.assertIsInstance(user.addresses[1], Address)
        self.assertEqual(len(user.addresses), 2)
        self.assertEqual(user.addresses[0]._data_dict, {'line1': 'London', 'line2': 'Road'})
        self.assertEqual(user.addresses[1]._data_dict, {'line1': 'Paris', 'line2': 'Road'})

    def test_instanceof_modifier_validates_instances_inside_list(self):
        @jsonclass(class_graph='test_instanceof_5')
        class Address:
            line1: str = types.str.required
            line2: str = types.str.required

        @jsonclass(class_graph='test_instanceof_5')
        class User:
            name: str = types.str
            addresses: List[Address] = types.listof(types.objof(Address))
        user = User(**{'name': 'John', 'addresses': [
            {'line1': 'London'},
            {'line1': 'Paris'},
        ]})
        self.assertRaises(ValidationException, user.validate)

    def test_instanceof_modifier_converts_to_json_inside_list(self):
        @jsonclass(class_graph='test_instanceof_6')
        class Address:
            line1: str = types.str
            line2: str = types.str

        @jsonclass(class_graph='test_instanceof_6')
        class User:
            name: str = types.str
            addresses: List[Address] = types.listof(types.objof(Address))
        user = User(**{'name': 'John', 'addresses': [
            {'line1': 'London', 'line2': 'Road'},
            {'line1': 'Paris', 'line2': 'Road'},
        ]})
        result = user.tojson()
        desired = {'name': 'John', 'addresses': [{'line1': 'London', 'line2': 'Road'}, {'line1': 'Paris', 'line2': 'Road'}]}
        self.assertEqual(result, desired)

    def test_instanceof_modifier_allow_argument_to_be_string(self):
        @jsonclass(class_graph='test_instanceof_7')
        class Post:
            title: str = types.str
            content: str = types.str
            author: User = types.objof('User')

        @jsonclass(class_graph='test_instanceof_7')
        class User:
            name: str = types.str
            posts: List[Post] = types.listof(types.objof('Post'))
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
        @jsonclass(class_graph='test_instanceof_8')
        class Staff:
            position: str
            user: User

        @jsonclass(class_graph='test_instanceof_8')
        class User:
            name: str = types.str
            staff: Staff
        user = User(**{'name': 'John', 'staff': {'position': 'CEO'}})
        self.assertIsInstance(user.staff, Staff)
        self.assertEqual(user.staff.position, 'CEO')
        staff = Staff(**{'position': 'Developer', 'user': {'name': 'Valy'}})
        self.assertIsInstance(staff.user, User)
        self.assertEqual(staff.user.name, 'Valy')

    def test_instanceof_works_in_list_without_assigning_a_types(self):
        @jsonclass(class_graph='test_instanceof_9')
        class Staff:
            position: str
            users: List[User]

        @jsonclass(class_graph='test_instanceof_9')
        class User:
            name: str
            staffs: List[Staff]
        user = User(**{'name': 'John', 'staffs': [{'position': 'CEO'}, {'position': 'CSO'}]})
        self.assertIsInstance(user.staffs[0], Staff)
        self.assertEqual(user.staffs[0].position, 'CEO')
        staff = Staff(**{'position': 'Developer', 'users': [{'name': 'Valy'}, {'name': 'Jonny'}]})
        self.assertIsInstance(staff.users[0], User)
        self.assertEqual(staff.users[0].name, 'Valy')

    def test_instanceof_works_in_dict_without_assigning_a_types(self):
        @jsonclass(class_graph='test_instanceof_10')
        class Staff:
            position: str
            users: Dict[str, User]

        @jsonclass(class_graph='test_instanceof_10')
        class User:
            name: str
            staffs: Dict[str, Staff]
        user = User(**{'name': 'John', 'staffs': {'a': {'position': 'CEO'}, 'b': {'position': 'CSO'}}})
        self.assertIsInstance(user.staffs['a'], Staff)
        self.assertEqual(user.staffs['a'].position, 'CEO')
        staff = Staff(**{'position': 'Developer', 'users': {'a': {'name': 'Valy'}, 'b': {'name': 'Jonny'}}})
        self.assertIsInstance(staff.users['a'], User)
        self.assertEqual(staff.users['a'].name, 'Valy')

    def test_instance_of_accepts_object(self):

        @jsonclass(class_graph='test_instanceof__1')
        class Staff:
            position: str
            user: User = types.linkto.objof('User').required

        @jsonclass(class_graph='test_instanceof__1')
        class User:
            name: str
            staff: Staff = types.objof('Staff').linkedby('user').required

        staff = Staff(position='CFO')
        user = User(name='John', staff=staff)
        self.assertEqual(user.staff.user, user)

    def test_instanceof_raises_if_strict_specified(self):
        @jsonclass(class_graph='test_instanceof_13')
        class Staff:
            position: str
            user: User = types.objof('User').required

        @jsonclass(class_graph='test_instanceof_13')
        class User:
            name: str
            staff: Staff = types.objof('Staff').strict.required
        with self.assertRaisesRegex(ValidationException, "key is not allowed"):
            User(**{'name': 'John', 'staff': {'position': 'CEO', 'boom': True}})

    def test_instanceof_raises_if_strict_instance(self):
        @jsonclass(class_graph='test_instanceof_14', strict_input=True)
        class Staff:
            position: str
            user: User = types.objof('User').required

        @jsonclass(class_graph='test_instanceof_14')
        class User:
            name: str
            staff: Staff = types.objof('Staff').required
        with self.assertRaisesRegex(ValidationException, "'staff\\.boom': key is not allowed"):
            User(**{'name': 'John', 'staff': {'position': 'CEO', 'boom': True}})

    def test_instanceof_create_circular_ref_for_local_and_foreign_binding(self):

        @jsonclass(class_graph='test_instanceof_15')
        class Staff:
            id: int = types.int.primary
            position: str
            user: User = types.linkto.objof('User').required

        @jsonclass(class_graph='test_instanceof_15')
        class User:
            id: int = types.int.primary
            name: str
            staff: Staff = types.objof('Staff').linkedby('user').required

        user = User(**{'id': 1, 'name': 'John', 'staff': {'id': 1, 'position': 'CEO'}})
        self.assertEqual(user.staff.user, user)

    def test_instanceof_create_circular_ref_for_foreign_and_local_binding(self):

        @jsonclass(class_graph='test_instanceof_16')
        class Staff:
            position: str
            user: User = types.objof('User').linkedby('staff').required

        @jsonclass(class_graph='test_instanceof_16')
        class User:
            name: str
            staff: Staff = types.linkto.objof('Staff').required

        user = User(**{'name': 'John', 'staff': {'position': 'CEO'}})
        self.assertEqual(user.staff.user, user)

    def test_instanceof_create_circular_ref_for_foreign_list_and_local_binding(self):

        @jsonclass(class_graph='test_instanceof_17')
        class Post:
            title: str
            user: User = types.linkto.objof('User').required

        @jsonclass(class_graph='test_instanceof_17')
        class User:
            name: str
            posts: List[Post] = types.listof('Post').linkedby('user').required

        user = User(**{'name': 'John', 'posts': [{'title': 'A'}, {'title': 'B'}]})
        self.assertEqual(user.posts[0].user, user)
        self.assertEqual(user.posts[1].user, user)

    def test_instanceof_create_circular_ref_for_local_list_and_foreign_binding(self):

        @jsonclass(class_graph='test_instanceof_18')
        class Post:
            title: str
            user: User = types.objof('User').linkedby('posts').required

        @jsonclass(class_graph='test_instanceof_18')
        class User:
            name: str
            posts: List[Post] = types.linkto.listof('Post').required

        user = User(**{'name': 'John', 'posts': [{'title': 'A'}, {'title': 'B'}]})
        self.assertEqual(user.posts[0].user, user)
        self.assertEqual(user.posts[1].user, user)

    def test_instanceof_create_circular_ref_for_foreign_item_and_local_list_binding(self):

        @jsonclass(class_graph='test_instanceof_19')
        class Post:
            title: str
            user: User = types.linkto.objof('User').required

        @jsonclass(class_graph='test_instanceof_19')
        class User:
            name: str
            posts: List[Post] = types.listof('Post').linkedby('user').required
        post = Post(**{'title': 'A', 'user': {'name': 'B'}})
        self.assertEqual(post.user.posts[0], post)

    def test_instanceof_create_circular_ref_for_local_list_and_foreign_item_binding(self):

        @jsonclass(class_graph='test_instanceof_20')
        class Post:
            title: str
            user: User = types.objof('User').linkedby('posts').required

        @jsonclass(class_graph='test_instanceof_20')
        class User:
            name: str
            posts: List[Post] = types.linkto.listof('Post').required

        post = Post(**{'title': 'A', 'user': {'name': 'B'}})
        self.assertEqual(post.user.posts[0], post)

    def test_instanceof_create_circular_ref_for_many_to_many(self):

        @jsonclass(class_graph='test_instanceof_21')
        class Book:
            title: str
            users: List[User] = types.listof('User').linkedthru('books').required

        @jsonclass(class_graph='test_instanceof_21')
        class User:
            name: str
            books: List[Book] = types.listof('Book').linkedthru('users').required

        book = Book(**{'title': 'A', 'users': [{'name': 'A'}, {'name': 'B'}]})
        self.assertEqual(book.users[0].books[0], book)
        self.assertEqual(book.users[1].books[0], book)

    def test_instanceof_circular_refs_create_refs_for_same_object(self):
        root_user = User(**input)
        self.assertEqual(root_user.name, 'U1')
        self.assertEqual(root_user.posts[0].name, 'P1')
        self.assertEqual(root_user.posts[1].name, 'P2')
        self.assertEqual(root_user.posts[0].comments[0].content, 'C1')
        self.assertEqual(root_user.posts[0].comments[1].content, 'C2')
        self.assertEqual(root_user.posts[0].comments[2].content, 'C3')
        self.assertEqual(root_user.posts[1].comments[0].content, 'C4')
        self.assertEqual(root_user.posts[1].comments[1].content, 'C5')
        self.assertIs(root_user.posts[0].user, root_user)
        self.assertIs(root_user.posts[1].user, root_user)
        self.assertIs(root_user.posts[0].comments[1].commenter, root_user)
        self.assertIs(root_user.posts[0].comments[1].parent,
                      root_user.posts[0].comments[0])
        self.assertIs(root_user.posts[0].comments[1],
                      root_user.posts[0].comments[0].children[0])
        commenter_u2_0 = root_user.posts[0].comments[0].commenter
        commenter_u2_1 = root_user.posts[0].comments[2].commenter
        commenter_u2_2 = root_user.posts[1].comments[0].commenter
        self.assertIs(commenter_u2_0, commenter_u2_1)
        self.assertIs(commenter_u2_1, commenter_u2_2)
        self.assertEqual(len(commenter_u2_1.comments), 3)
        self.assertIs(commenter_u2_1.comments[0],
                      root_user.posts[0].comments[0])
        self.assertIs(commenter_u2_1.comments[1],
                      root_user.posts[0].comments[2])
        self.assertIs(commenter_u2_1.comments[2],
                      root_user.posts[1].comments[0])
        commenter_u3 = root_user.posts[1].comments[1].commenter
        self.assertIs(root_user.posts[1].comments[1], commenter_u3.comments[0])
        self.assertEqual(1, len(root_user.comments))
        self.assertIs(root_user.comments[0], root_user.posts[0].comments[1])

    def test_instanceof_circular_refs_validate_do_not_infinite_loop(self):
        root_user = User(**input)
        root_user.validate()

    def test_instanceof_circular_refs_tojson_do_not_infinite_loop(self):
        root_user = User(**input)
        json = root_user.tojson(reverse_relationship=False)
        result = {'comments': [{'children': None,
               'commenterId': 1,
               'content': 'C2',
               'id': 2,
               'parent': {'commenterId': 2,
                          'content': 'C1',
                          'id': 1,
                          'parentId': None,
                          'postId': 1},
               'parentId': 1,
               'postId': 1}],
            'id': 1,
            'name': 'U1',
            'posts': [{'comments': [{'children': [{'commenterId': 1,
                                        'content': 'C2',
                                        'id': 2,
                                        'parentId': 1,
                                        'postId': 1}],
                          'commenterId': 2,
                          'content': 'C1',
                          'id': 1,
                          'parent': None,
                          'parentId': None,
                          'postId': 1},
                         {'children': None,
                          'commenterId': 1,
                          'content': 'C2',
                          'id': 2,
                          'parent': {'commenterId': 2,
                                     'content': 'C1',
                                     'id': 1,
                                     'parentId': None,
                                     'postId': 1},
                          'parentId': 1,
                          'postId': 1},
                         {'children': None,
                          'commenterId': 2,
                          'content': 'C3',
                          'id': 3,
                          'parent': None,
                          'parentId': None,
                          'postId': 1}],
            'id': 1,
            'name': 'P1',
            'userId': 1},
           {'comments': [{'children': None,
                          'commenterId': 2,
                          'content': 'C4',
                          'id': 4,
                          'parent': None,
                          'parentId': None,
                          'postId': 2},
                         {'children': None,
                          'commenterId': 3,
                          'content': 'C5',
                          'id': 5,
                          'parent': None,
                          'parentId': None,
                          'postId': 2}],
            'id': 2,
            'name': 'P2',
            'userId': 1}]}
        self.assertEqual(json, result)

    def test_instanceof_circular_refs_tojson_with_rr_do_not_infinite_loop(self):
        root_user = User(**input)
        json = root_user.tojson(reverse_relationship=True)
        result = {'comments': [{'children': None,
               'commenter': {'id': 1, 'name': 'U1'},
               'commenterId': 1,
               'content': 'C2',
               'id': 2,
               'parent': {'commenterId': 2,
                          'content': 'C1',
                          'id': 1,
                          'parentId': None,
                          'postId': 1},
               'parentId': 1,
               'post': {'comments': [{'commenterId': 2,
                                      'content': 'C1',
                                      'id': 1,
                                      'parentId': None,
                                      'postId': 1},
                                     {'commenterId': 1,
                                      'content': 'C2',
                                      'id': 2,
                                      'parentId': 1,
                                      'postId': 1},
                                     {'commenterId': 2,
                                      'content': 'C3',
                                      'id': 3,
                                      'parentId': None,
                                      'postId': 1}],
                        'id': 1,
                        'name': 'P1',
                        'user': {'id': 1, 'name': 'U1'},
                        'userId': 1},
               'postId': 1}],
            'id': 1,
            'name': 'U1',
            'posts': [{'comments': [{'children': [{'commenterId': 1,
                                        'content': 'C2',
                                        'id': 2,
                                        'parentId': 1,
                                        'postId': 1}],
                          'commenter': {'id': 2, 'name': 'U2'},
                          'commenterId': 2,
                          'content': 'C1',
                          'id': 1,
                          'parent': None,
                          'parentId': None,
                          'post': {'id': 1, 'name': 'P1', 'userId': 1},
                          'postId': 1},
                         {'children': None,
                          'commenter': {'id': 1, 'name': 'U1'},
                          'commenterId': 1,
                          'content': 'C2',
                          'id': 2,
                          'parent': {'commenterId': 2,
                                     'content': 'C1',
                                     'id': 1,
                                     'parentId': None,
                                     'postId': 1},
                          'parentId': 1,
                          'post': {'id': 1, 'name': 'P1', 'userId': 1},
                          'postId': 1},
                         {'children': None,
                          'commenter': {'id': 2, 'name': 'U2'},
                          'commenterId': 2,
                          'content': 'C3',
                          'id': 3,
                          'parent': None,
                          'parentId': None,
                          'post': {'id': 1, 'name': 'P1', 'userId': 1},
                          'postId': 1}],
            'id': 1,
            'name': 'P1',
            'user': {'id': 1, 'name': 'U1'},
            'userId': 1},
           {'comments': [{'children': None,
                          'commenter': {'id': 2, 'name': 'U2'},
                          'commenterId': 2,
                          'content': 'C4',
                          'id': 4,
                          'parent': None,
                          'parentId': None,
                          'post': {'id': 2, 'name': 'P2', 'userId': 1},
                          'postId': 2},
                         {'children': None,
                          'commenter': {'id': 3, 'name': 'U3'},
                          'commenterId': 3,
                          'content': 'C5',
                          'id': 5,
                          'parent': None,
                          'parentId': None,
                          'post': {'id': 2, 'name': 'P2', 'userId': 1},
                          'postId': 2}],
            'id': 2,
            'name': 'P2',
            'user': {'id': 1, 'name': 'U1'},
            'userId': 1}]}
        self.assertEqual(json, result)
