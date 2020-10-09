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


@jsonclass(graph='test_json_object_assign')
class Post(JSONObject):
    id: int
    name: str
    author: Author = types.linkto.instanceof('Author').required


@jsonclass(graph='test_json_object_assign')
class Author(JSONObject):
    id: int
    name: str
    posts: list[Post] = types.listof('Post').linkedby('author').required


@jsonclass(graph='test_json_object_assign')
class Customer(JSONObject):
    id: int
    name: str
    products: list[Product] = (types.listof('Product').nonnull
                               .linkedthru('customers').required)


@jsonclass(graph='test_json_object_assign')
class Product(JSONObject):
    id: int
    name: str
    customers: list[Customer] = (types.listof('Customer').nonnull
                                 .linkedthru('products').required)


class TestJSONObjectReferenceHook(TestCase):

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

    def test_json_objects_disconnects_1k_1l_thru_assign(self):
        staff = Staff(id=1, position='CEO')
        user = User(id=1, name='Victor')
        user.staff = staff
        user.staff = None
        self.assertEqual(user.staff, None)
        self.assertEqual(staff.user, None)

    def test_json_objects_disconnects_1l_1k_thru_assign(self):
        staff = Staff(id=1, position='CEO')
        user = User(id=1, name='Victor')
        staff.user = user
        staff.user = None
        self.assertEqual(user.staff, None)
        self.assertEqual(staff.user, None)

    def test_json_objects_disconnects_1_many_empty_thru_assign(self):
        post = Post(id=1, name='Zayton City')
        author = Author(id=1, name='Victor')
        post.author = author
        post.author = None
        self.assertEqual(len(author.posts), 0)
        self.assertEqual(post.author, None)

    def test_json_objects_disconnects_1_many_one_exist_thru_assign(self):
        post = Post(id=1, name='Zayton City')
        author = Author(id=1, name='Victor')
        post.author = author
        post2 = Post(id=2, name='Chinkang City')
        post2.author = author
        post.author = None
        self.assertEqual(len(author.posts), 1)
        self.assertEqual(post2.author.posts[0], post2)
        self.assertEqual(author.posts[0].author, author)
        self.assertEqual(post.author, None)
        self.assertEqual(post2.author, author)

    def test_json_objects_connects_many_1_thru_assign(self):
        post1 = Post(id=1, name='Zayton City')
        post2 = Post(id=2, name='Teochew City')
        author = Author(id=1, name='Victor')
        author.posts = [post1, post2]
        self.assertEqual(len(author.posts), 2)
        self.assertEqual(post1.author, author)
        self.assertEqual(post2.author, author)

    def test_json_objects_disconnects_many_1_thru_assign_empty_list(self):
        post1 = Post(id=1, name='Zayton City')
        post2 = Post(id=2, name='Teochew City')
        author = Author(id=1, name='Victor')
        author.posts = [post1, post2]
        author.posts = []
        self.assertEqual(len(author.posts), 0)
        self.assertEqual(post1.author, None)
        self.assertEqual(post2.author, None)

    def test_json_objects_connects_1_many_thru_list_add(self):
        post1 = Post(id=1, name='Zayton City')
        post2 = Post(id=2, name='Teochew City')
        author = Author(id=1, name='Victor')
        author.posts = []
        author.posts.append(post1)
        author.posts.insert(1, post2)
        self.assertEqual(len(author.posts), 2)
        self.assertEqual(post1.author, author)
        self.assertEqual(post2.author, author)

    def test_json_objects_disconnects_1_many_thru_list_del(self):
        post1 = Post(id=1, name='Zayton City')
        post2 = Post(id=2, name='Teochew City')
        author = Author(id=1, name='Victor')
        author.posts = [post1, post2]
        del author.posts[0]
        self.assertEqual(len(author.posts), 1)
        self.assertEqual(post1.author, None)
        self.assertEqual(post2.author, author)

    def test_json_objects_connects_many_many_thru_list_add(self):
        customer1 = Customer(id=1, name='Customer John', products=[])
        customer2 = Customer(id=2, name='Customer Peter', products=[])
        product1 = Product(id=1, name='PS5', customers=[])
        product2 = Product(id=1, name='Xbox', customers=[])
        customer1.products.append(product1)
        customer1.products.append(product2)
        customer2.products.extend([product1, product2])
        self.assertEqual(customer1.products, [product1, product2])
        self.assertEqual(customer2.products, [product1, product2])
        self.assertEqual(product1.customers, [customer1, customer2])
        self.assertEqual(product2.customers, [customer1, customer2])

    def test_json_objects_disconnects_many_many_thru_list_del(self):
        product1 = Product(id=1, name='PS5')
        product2 = Product(id=1, name='Xbox')
        customer1 = Customer(id=1, name='Customer John',
                             products=[product1, product2])
        customer2 = Customer(id=2, name='Customer Peter',
                             products=[product1, product2])
        customer1.products.clear()
        self.assertEqual(customer1.products, [])
        self.assertEqual(customer2.products, [product1, product2])
        self.assertEqual(product1.customers, [customer2])
        self.assertEqual(product2.customers, [customer2])

    def test_json_objects_connects_many_many_reassign(self):
        customer1 = Customer(id=1, name='Customer John', products=[])
        customer2 = Customer(id=2, name='Customer Peter', products=[])
        product1 = Product(id=1, name='PS5', customers=[])
        product2 = Product(id=1, name='Xbox', customers=[])
        customer1.products.append(product1)
        customer1.products.append(product2)
        customer2.products.extend([product1, product2])
        customer1.products = [product1, product2]
        self.assertEqual(customer1.products, [product1, product2])
        self.assertEqual(customer2.products, [product1, product2])
        self.assertEqual(product1.customers, [customer2, customer1])
        self.assertEqual(product2.customers, [customer1, customer2])

    def test_json_objects_connects_1_1_reassign(self):
        staff1 = Staff(id=1, position='CEO')
        staff2 = Staff(id=2, position='CFO')
        user = User(id=1, name='Victor')
        user.staff = staff1
        user.staff = staff2
        self.assertEqual(staff1.user, None)
        self.assertEqual(staff2.user, user)
        self.assertEqual(user.staff, staff2)
