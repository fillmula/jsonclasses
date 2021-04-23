from __future__ import annotations
from unittest import TestCase
from tests.classes.user_sos import UserSOS, UserSOSZ
from tests.classes.linked_sos import (LinkedUserSOS, LinkedBookSOS,
                                      LinkedUserSOSE, LinkedBookSOSE)


class TestSetOnSave(TestCase):

    def test_new_object_triggers_setonsave(self):
        user = UserSOS(name='n', age=50)
        user._set_on_save()
        self.assertEqual(user.age, 350)

    def test_modified_object_triggers_setonsave(self):
        user = UserSOS(name='n', age=100)
        setattr(user, '_is_new', False)
        user.name = 'N'
        user._set_on_save()
        self.assertEqual(user.age, 400)

    def test_unmodified_object_wont_trigger_setonsave(self):
        user = UserSOS(name='n', age=100)
        setattr(user, '_is_new', False)
        user._set_on_save()
        self.assertEqual(user.age, 100)

    def test_setonsave_accepts_0_args(self):
        user = UserSOSZ(name='n', age=100)
        setattr(user, '_is_new', False)
        user.name = 'N'
        user._set_on_save()
        self.assertEqual(user.age, 500)

    def test_setonsave_triggers_for_modified_linked_objects(self):
        book1 = LinkedBookSOS(id=1, name='B1', value=1)
        book2 = LinkedBookSOS(id=2, name='B2', value=1)
        setattr(book1, '_is_new', False)
        setattr(book2, '_is_new', False)
        user = LinkedUserSOS(id=1, name='U', value=1)
        setattr(user, '_is_new', False)
        user.books.append(book1)
        user.books.append(book2)
        user._set_on_save()
        self.assertEqual(user.value, 2)
        self.assertEqual(book1.value, 2)
        self.assertEqual(book2.value, 2)

    def test_setonsave_triggers_even_root_is_unmodified(self):
        book1 = LinkedBookSOS(id=1, name='B1', value=1)
        book2 = LinkedBookSOS(id=2, name='B2', value=1)
        setattr(book1, '_is_new', False)
        setattr(book2, '_is_new', False)
        user = LinkedUserSOS(id=1, name='U', value=1)
        setattr(user, '_is_new', False)
        user.books.append(book1)
        user.books.append(book2)
        setattr(user, '_is_modified', False)
        setattr(user, '_modified_fields', set())
        user._set_on_save()
        self.assertEqual(user.value, 1)
        self.assertEqual(book1.value, 2)
        self.assertEqual(book2.value, 2)

    def test_setonsave_triggers_anyway_if_owner_modified_for_embedded(self):
        book1 = LinkedBookSOSE(id=1, name='B1', value=1)
        book2 = LinkedBookSOSE(id=2, name='B2', value=1)
        setattr(book1, '_is_new', False)
        setattr(book2, '_is_new', False)
        user = LinkedUserSOSE(id=1, name='U', value=1, books=[book1, book2])
        book1.name = 'BB1'
        book2.name = 'BB2'
        setattr(user, '_is_modified', False)
        setattr(user, '_modified_fields', set())
        user._set_on_save()
        self.assertEqual(user.value, 2)
        self.assertEqual(book1.value, 2)
        self.assertEqual(book2.value, 2)

    def test_setonsave_triggers_anyway_if_owner_unmodified_for_embedded(self):
        book1 = LinkedBookSOSE(id=1, name='B1', value=1)
        book2 = LinkedBookSOSE(id=2, name='B2', value=1)
        setattr(book1, '_is_new', False)
        setattr(book2, '_is_new', False)
        user = LinkedUserSOSE(id=1, name='U', value=1, books=[book1, book2])
        book1.name = 'BB1'
        book2.name = 'BB2'
        setattr(user, '_is_new', False)
        setattr(user, '_is_modified', False)
        setattr(user, '_modified_fields', set())
        user._set_on_save()
        self.assertEqual(user.value, 1)
        self.assertEqual(book1.value, 2)
        self.assertEqual(book2.value, 2)
