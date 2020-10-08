from __future__ import annotations
from typing import List
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


@jsonclass(graph='test_json_object_assign')
class Post(JSONObject):
    id: int
    name: str
    author: Author = types.linkto.instanceof('Author').required


@jsonclass(graph='test_json_object_assign')
class Author(JSONObject):
    id: int
    name: str
    posts: List[Post] = types.listof('Post').linkedby('author').required


class TestJSONObjectAssign(TestCase):

    def test_json_objects_connects_1k_1l_thru_assign(self):
        staff = Staff(id=1, position='CEO')
        user = User(id=1, name='Victor')
        user.staff = staff
        self.assertEqual(user.staff.user, user)
        self.assertEqual(staff.user.staff, staff)

    def test_json_objects_connects_1l_1k_thru_assign(self):
        staff = Staff(id=1, position='CEO')
        user = User(id=1, name='Victor')
        staff.user = user
        self.assertEqual(user.staff.user, user)
        self.assertEqual(staff.user.staff, staff)

    def test_json_objects_connects_1_many_empty_thru_assign(self):
        post = Post(id=1, name='Zayton City')
        author = Author(id=1, name='Victor')
        post.author = author
        self.assertEqual(len(author.posts), 1)
        self.assertEqual(post.author.posts[0], post)
        self.assertEqual(author.posts[0].author, author)
        post.author = author
        self.assertEqual(len(author.posts), 1)
        self.assertEqual(post.author.posts[0], post)
        self.assertEqual(author.posts[0].author, author)

    def test_json_objects_connects_1_many_one_exist_thru_assign(self):
        post = Post(id=1, name='Zayton City')
        author = Author(id=1, name='Victor')
        post.author = author
        post2 = Post(id=2, name='Chinkang City')
        post2.author = author
        self.assertEqual(len(author.posts), 2)
        self.assertEqual(post.author.posts[1], post2)
        self.assertEqual(author.posts[1].author, author)
        post2.author = author
        self.assertEqual(len(author.posts), 2)
        self.assertEqual(post.author.posts[1], post2)
        self.assertEqual(author.posts[1].author, author)
