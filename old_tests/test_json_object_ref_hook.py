from __future__ import annotations
from unittest import TestCase
from jsonclasses import jsonclass, JSONObject, types


@jsonclass(class_graph='test_json_object_assign')
class Staff(JSONObject):
    id: int = types.int.primary
    position: str
    user: User = types.linkto.instanceof('User').required


@jsonclass(class_graph='test_json_object_assign')
class User(JSONObject):
    id: int = types.int.primary
    name: str
    staff: Staff = types.instanceof('Staff').linkedby('user').required


@jsonclass(class_graph='test_json_object_assign')
class Post(JSONObject):
    id: int = types.int.primary
    name: str
    author: Author = types.linkto.instanceof('Author').required


@jsonclass(class_graph='test_json_object_assign')
class Author(JSONObject):
    id: int = types.int.primary
    name: str
    posts: list[Post] = types.listof('Post').linkedby('author').required


@jsonclass(class_graph='test_json_object_assign')
class Customer(JSONObject):
    id: int = types.int.primary
    name: str
    products: list[Product] = (types.listof('Product').nonnull
                               .linkedthru('customers').required)


@jsonclass(class_graph='test_json_object_assign')
class Product(JSONObject):
    id: int = types.int.primary
    name: str
    customers: list[Customer] = (types.listof('Customer').nonnull
                                 .linkedthru('products').required)


class TestJSONObjectReferenceHook(TestCase):

    def test_json_objects_connects_many_many_reassign(self):
        customer1 = Customer(id=1, name='Customer John', products=[])
        customer2 = Customer(id=2, name='Customer Peter', products=[])
        product1 = Product(id=1, name='PS5', customers=[])
        product2 = Product(id=2, name='Xbox', customers=[])
        customer1.products.extend([product1, product2])
        customer2.products.extend([product1, product2])
        customer1.products = [product1, product2]
        self.assertEqual(customer1.products, [product1, product2])
        self.assertEqual(customer2.products, [product1, product2])
        self.assertEqual(product1.customers, [customer2, customer1])
        self.assertEqual(product2.customers, [customer2, customer1])

    def test_json_objects_connects_1_1_reassign(self):
        staff1 = Staff(id=1, position='CEO')
        staff2 = Staff(id=2, position='CFO')
        user = User(id=1, name='Victor')
        user.staff = staff1
        user.staff = staff2
        self.assertEqual(staff1.user, None)
        self.assertEqual(staff2.user, user)
        self.assertEqual(user.staff, staff2)
