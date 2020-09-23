# from __future__ import annotations
# from typing import List
# import unittest
# from jsonclasses import jsonclass, PersistableJSONObject, types
# from datetime import datetime


# class TestPersistableJSONObject(unittest.TestCase):

#     def test_persistable_json_object_has_created_at_on_initializing(self):
#         o = PersistableJSONObject()
#         self.assertTrue(type(o.created_at) is datetime)
#         self.assertTrue(o.created_at < datetime.now())

#     def test_persistable_json_object_has_updated_at_on_initializing(self):
#         o = PersistableJSONObject()
#         self.assertTrue(type(o.updated_at) is datetime)
#         self.assertTrue(o.updated_at < datetime.now())

#     def test_persistable_json_object_has_id_with_default_value_none(self):
#         o = PersistableJSONObject()
#         self.assertTrue(o.id is None)

#     def test_persistable_json_object_id_can_be_int(self):
#         o = PersistableJSONObject()
#         o.id = 5
#         self.assertTrue(o.is_valid())

#     def test_persistable_json_object_id_can_be_str(self):
#         o = PersistableJSONObject()
#         o.id = "sbd"
#         self.assertTrue(o.is_valid())

#     def test_persistable_json_object_id_can_be_none(self):
#         o = PersistableJSONObject()
#         o.id = None
#         self.assertTrue(o.is_valid())

#     def test_persistable_json_object_has_timestamps_in_nested_instances(self):
#         @jsonclass(graph='test_persistable_json_01')
#         class TestAuthor(PersistableJSONObject):
#             name: str
#             posts: List[TestPost] = types.listof('TestPost').linkedby('author')

#         @jsonclass(graph='test_persistable_json_01')
#         class TestPost(PersistableJSONObject):
#             title: str
#             content: str
#             author: TestAuthor = types.linkto.instanceof(TestAuthor)
#         input = {
#             'name': 'John Lesque',
#             'posts': [
#                 {
#                     'title': 'Post One',
#                     'content': 'Great Article on Python.'
#                 },
#                 {
#                     'title': 'Post Two',
#                     'content': 'Great Article on JSON Classes.'
#                 }
#             ]
#         }
#         author = TestAuthor(**input)
#         self.assertIs(type(author.created_at), datetime)
#         self.assertIs(type(author.updated_at), datetime)
#         self.assertIs(type(author.posts[0].created_at), datetime)
#         self.assertIs(type(author.posts[0].updated_at), datetime)
#         self.assertIs(type(author.posts[1].created_at), datetime)
#         self.assertIs(type(author.posts[1].updated_at), datetime)
