"""تست‌های API + تست N+1 با assertNumQueries."""

from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from .models import (
    Brand,
    Category,
    Comment,
    Customer,
    Product,
    WishList,
)

User = get_user_model()


class ProductAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.brand = Brand.objects.create(name="Rolex")
        self.category = Category.objects.create(title="Classic")

        self.product1 = Product.objects.create(
            title="Rolex Submariner",
            brand=self.brand,
            category=self.category,
            price=Decimal("100.00"),
            is_special=True,
            is_luxury=True,
            is_available=True,
            stash=5,
        )
        self.product2 = Product.objects.create(
            title="Omega Speedmaster",
            brand=self.brand,
            category=self.category,
            price=Decimal("200.00"),
            is_special=True,
            is_luxury=True,
            is_available=True,
            stash=3,
        )
        self.product3 = Product.objects.create(
            title="TAG Heuer Carrera",
            brand=self.brand,
            category=self.category,
            price=Decimal("300.00"),
            is_special=False,
            is_luxury=True,
            is_available=True,
            stash=2,
        )

        self.user = User.objects.create_user(
            username="customer1",
            email="customer1@example.com",
            password="pass12345",
        )
        self.customer = Customer.objects.create(
            user=self.user,
            phone_number="09120000001",
        )
        WishList.objects.create(customer=self.customer, product=self.product1)
        Comment.objects.create(
            customer=self.customer,
            product=self.product1,
            body="عالی بود",
        )

    def test_product_list_fields_and_no_n_plus_one(self):
        with self.assertNumQueries(1):
            response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        first = response.data[0]
        self.assertIn("brand_name", first)
        self.assertIn("category_name", first)
        self.assertIn("stash", first)
        self.assertNotIn("description", first)

    def test_product_detail_click_count_and_no_n_plus_one(self):
        with self.assertNumQueries(5):
            first = self.client.get(f"/api/products/{self.product1.slug}/")

        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.data["click_count"], 1)
        self.assertEqual(len(first.data["comments"]), 1)

        with self.assertNumQueries(5):
            second = self.client.get(f"/api/products/{self.product1.slug}/")

        self.assertEqual(second.data["click_count"], 2)

    def test_luxury_special_average_and_no_n_plus_one(self):
        with self.assertNumQueries(2):
            response = self.client.get("/api/luxury-special/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(
            Decimal(response.data["average_luxury_price"]), Decimal("200.00")
        )

    def test_wishlist_requires_authentication(self):
        response = self.client.get("/api/me/wishlist/")
        self.assertIn(response.status_code, (401, 403))

    def test_wishlist_no_n_plus_one(self):
        self.client.force_authenticate(user=self.user)

        with self.assertNumQueries(1):
            response = self.client.get("/api/me/wishlist/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["product"]["title"], "Rolex Submariner")
        self.assertEqual(response.data[0]["customer"]["phone_number"], "09120000001")
