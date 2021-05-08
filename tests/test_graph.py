from __future__ import annotations
from datetime import datetime
from unittest import TestCase
from tests.classes.blog import User, Post


class TestGraph(TestCase):

    def test_graph_is_assigned_on_create(self):
        user = User(id=1, name='Phuê Ê')
        self.assertEqual(user._graph.get(user), user)
        objects = [object for object in user._graph]
        self.assertEqual(objects, [user])

    def test_graph_is_merged_on_connect(self):
        user = User(id=1, name='Phuê Ê')
        post = Post(id=1, name='M Tsai Tai Kha Kui Ê Lang')
        user.posts.append(post)
        self.assertEqual(user._graph, post._graph)
        self.assertEqual(user._graph.get(user), user)
        self.assertEqual(user._graph.get(post), post)
        objects = [object for object in user._graph]
        self.assertEqual(objects, [post, user])

    def test_graph_is_merged_on_init(self):
        post = Post(id=1, name='Tsih Ma Khai Si',
                    updated_at=datetime(2021, 3, 10, 0, 0, 0))
        user = User(id=1, name='Tsu Iu Tsu Tsai', posts=[post])
        self.assertEqual(user._graph, post._graph)
        self.assertEqual(user._graph.get(user), user)
        self.assertEqual(user._graph.get(post), post)
        objects = [object for object in user._graph]
        self.assertEqual(objects, [user, post])

    def test_graph_on_conflict_keep_new_one(self):
        post = Post(id=1, name='M Tsai Tai Kha Kui Ê Lang',
                    updated_at=datetime(2021, 3, 10, 0, 0, 0))
        user = User(id=1, name='Phuê Ê')
        user.posts = [post]
        user._mark_not_new()
        post._mark_not_new()
        post_new = Post(id=1, name='Koh Kin Tiu Koh Tsin Ki Thai',
                        updated_at=datetime(2021, 3, 11, 0, 0, 0))
        post_new._mark_not_new()
        user.posts = [post_new]
        self.assertEqual(user._graph, post_new._graph)
        self.assertEqual(user._graph.get(user), user)
        self.assertEqual(user._graph.get(post), post_new)
        objects = [object for object in user._graph]
        self.assertEqual(objects, [post_new, user])
        self.assertEqual(user.posts, [post_new])
        self.assertEqual(post.is_outdated, True)
        self.assertEqual(post_new.is_outdated, False)

    def test_graph_on_conflict_keep_edited_one(self):
        post = Post(id=1, name='M Tsai Tai Kha Kui Ê Lang',
                    updated_at=datetime(2021, 3, 10, 0, 0, 0))
        user = User(id=1, name='Phuê Ê')
        user.posts = [post]
        user._mark_not_new()
        post._mark_not_new()
        post_new = Post(id=1, name='Koh Kin Tiu Koh Tsin Ki Thai',
                        updated_at=datetime(2021, 3, 10, 0, 0, 0))
        post_new._mark_not_new()
        user.posts = [post_new]
        post_new.name = 'Tioh Si Bu Tai'
        self.assertEqual(user._graph, post_new._graph)
        self.assertEqual(user._graph.get(user), user)
        self.assertEqual(user._graph.get(post), post_new)
        objects = [object for object in user._graph]
        self.assertEqual(objects, [post_new, user])
        self.assertEqual(user.posts, [post_new])
        self.assertEqual(post.is_outdated, True)
        self.assertEqual(post_new.is_outdated, False)
