from __future__ import annotations
from typing import Optional
from unittest import TestCase
from jsonclasses import jsonclass, JSONObject, types, Link, linkedby, linkto


@jsonclass(class_graph='test_object_graph_1')
class Contact(JSONObject):
    id: int = types.int.primary.required
    name: str
    address: Link[Address, linkedby('contact')]


@jsonclass(class_graph='test_object_graph_1')
class Address(JSONObject):
    id: int = types.int.primary.required
    line1: str
    contact: Link[Contact, linkto]


@jsonclass(class_graph='test_object_graph_1')
class User(JSONObject):
    id: int = types.int.primary.required
    name: str
    posts: list[Post] = types.listof('Post').linkedby('user').required
    comments: list[Comment] = types.listof('Comment').linkedby('commenter').required


@jsonclass(class_graph='test_object_graph_1')
class Post(JSONObject):
    id: int = types.int.primary.required
    name: str
    user: User = types.linkto.instanceof('User').required
    comments: list[Comment] = types.listof('Comment').linkedby('post').required


@jsonclass(class_graph='test_object_graph_1')
class Comment(JSONObject):
    id: int = types.int.primary.required
    content: str
    post: Post = types.linkto.instanceof('Post').required
    parent: Optional[Comment] = types.linkto.instanceof('Comment')
    children: list[Comment] = types.listof('Comment').linkedby('parent').required
    commenter: User = types.linkto.instanceof('User').required


class TestObjectGraph(TestCase):

    def test_new_object_has_graph_and_itself_is_on_it(self):
        contact = Contact(id=1, name='John')
        for o in contact._graph:
            self.assertEqual(o, contact)

    def test_merge_object_graph_on_assign(self):
        contact = Contact(id=1, name='John')
        address = Address(id=1, line1='Line 1')
        contact.address = address
        self.assertEqual(contact._graph, address._graph)
