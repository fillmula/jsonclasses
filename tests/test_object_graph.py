from __future__ import annotations
from typing import Optional
from unittest import TestCase
from jsonclasses import (jsonclass, JSONObject, ORMObject, types, Link,
                         linkedby, linkto)


@jsonclass(class_graph='test_object_graph_1')
class Contact(ORMObject):
    id: Optional[int] = types.int.primary
    name: str
    address: Link[Address, linkedby('contact')]


@jsonclass(class_graph='test_object_graph_1')
class Address(ORMObject):
    id: Optional[int] = types.int.primary
    line1: str
    contact: Link[Contact, linkto]


@jsonclass(class_graph='test_object_graph_1')
class User(JSONObject):
    id: int = types.int.primary.required
    name: str
    posts: list[Post] = types.nonnull.listof('Post').linkedby('user').required
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

    def test_merge_object_graph_on_list_assign(self):
        user = User(id=1, name='John')
        post = Post(id=1, name='P1')
        user.posts = [post]
        self.assertEqual(user._graph, post._graph)

    def test_merge_object_graph_on_list_append(self):
        user = User(id=1, name='John')
        post = Post(id=1, name='P1')
        user.posts.append(post)
        self.assertEqual(user._graph, post._graph)

    def test_referenced_objects_validate_dont_get_circular_without_pk(self):
        contact = Contact(name='John')
        address = Address(line1='Line 1')
        contact.address = address
        contact.validate()

    def test_referenced_objects_tojson_dont_get_circular_without_pk(self):
        contact = Contact(name='John')
        address = Address(line1='Line 1')
        contact.address = address
        self.assertEqual(contact.tojson(), {
            'id': None, 'name': 'John', 'address': {
                'id': None, 'line1': 'Line 1', 'contact': {
                    'id': None, 'name': 'John'}}})

    def test_referenced_objects_serialize_dont_get_circular_without_pk(self):
        contact = Contact(name='John')
        address = Address(line1='Line 1')
        contact.address = address
        contact._setonsave()
