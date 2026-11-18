from decimal import Decimal
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Category, Product


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic gadgets and devices",
        )

    def test_category_creation_and_str(self):
        self.assertEqual(str(self.category), "Electronics")
        self.assertEqual(self.category.name, "Electronics")
        self.assertEqual(self.category.description, "Electronic gadgets and devices")
        self.assertIsNotNone(self.category.created_at)
        self.assertIsNotNone(self.category.updated_at)


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Electronics",
            description="Electronic gadgets and devices",
        )
        self.product = Product.objects.create(
            category=self.category,
            name="Wireless Headphones",
            description="Noise-cancelling over-ear headphones",
            price=Decimal("99.99"),
            stock_quantity=50,
            is_active=True,
        )

    def test_product_creation_and_str(self):
        self.assertEqual(str(self.product), "Wireless Headphones")
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.price, Decimal("99.99"))
        self.assertEqual(self.product.stock_quantity, 50)
        self.assertTrue(self.product.is_active)

    def test_category_protection_on_delete(self):
        # Category cannot be deleted if it has related products (PROTECT)
        with self.assertRaises(ProtectedError):
            self.category.delete()


class CategoryAPITests(APITestCase):
    def setUp(self):
        self.category1 = Category.objects.create(name="Books", description="All kinds of books")
        self.category2 = Category.objects.create(name="Clothing", description="Apparel and fashion")
        self.list_url = reverse("products:category-list")
        self.detail_url = reverse("products:category-detail", kwargs={"pk": self.category1.pk})

    def test_list_categories(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_category(self):
        payload = {"name": "Home & Kitchen", "description": "Appliances and utensils"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Home & Kitchen")
        self.assertTrue(Category.objects.filter(name="Home & Kitchen").exists())

    def test_create_duplicate_category_fails(self):
        payload = {"name": "Books", "description": "Duplicate category"}
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_category(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category1.name)

    def test_update_category(self):
        payload = {"name": "Literature", "description": "Classic and modern literature"}
        response = self.client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, "Literature")

    def test_delete_category(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category1.pk).exists())


class ProductAPITests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Electronics", description="Gadgets")
        self.product = Product.objects.create(
            category=self.category,
            name="Laptop",
            description="Powerful laptop",
            price=Decimal("1200.00"),
            stock_quantity=10,
            is_active=True,
        )
        self.list_url = reverse("products:product-list")
        self.detail_url = reverse("products:product-detail", kwargs={"pk": self.product.pk})

    def test_list_products(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Laptop")
        self.assertEqual(response.data[0]["category_name"], "Electronics")

    def test_create_product(self):
        payload = {
            "category": self.category.id,
            "name": "Smartphone",
            "description": "Latest model smartphone",
            "price": "699.99",
            "stock_quantity": 25,
            "is_active": True,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Smartphone")
        self.assertEqual(response.data["category_name"], "Electronics")
        self.assertTrue(Product.objects.filter(name="Smartphone").exists())

    def test_create_product_missing_category(self):
        payload = {
            "name": "Smartphone Without Category",
            "price": "699.99",
            "stock_quantity": 25,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_product(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Laptop")
        self.assertEqual(response.data["category_name"], "Electronics")

    def test_update_product(self):
        payload = {
            "category": self.category.id,
            "name": "Gaming Laptop",
            "description": "High performance gaming laptop",
            "price": "1500.00",
            "stock_quantity": 5,
            "is_active": True,
        }
        response = self.client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Gaming Laptop")
        self.assertEqual(self.product.price, Decimal("1500.00"))

    def test_delete_product(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
