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
        self.invalid_detail_url = reverse("products:category-detail", kwargs={"pk": 99999})

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

    def test_create_category_invalid_input(self):
        # Missing required name field
        response = self.client.post(self.list_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

        # Blank name
        response = self.client.post(self.list_url, {"name": ""}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)

    def test_retrieve_category(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category1.name)

    def test_retrieve_invalid_category_id_returns_404(self):
        response = self.client.get(self.invalid_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)

    def test_update_category(self):
        payload = {"name": "Literature", "description": "Classic and modern literature"}
        response = self.client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, "Literature")

    def test_partial_update_category_patch(self):
        payload = {"description": "Updated description via PATCH"}
        response = self.client.patch(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.description, "Updated description via PATCH")
        self.assertEqual(self.category1.name, "Books")

    def test_update_invalid_category_id_returns_404(self):
        payload = {"name": "Non-existent", "description": "Does not exist"}
        response = self.client.put(self.invalid_detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_category(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category1.pk).exists())

    def test_delete_invalid_category_id_returns_404(self):
        response = self.client.delete(self.invalid_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
        self.invalid_detail_url = reverse("products:product-detail", kwargs={"pk": 99999})

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

    def test_create_product_missing_required_fields(self):
        response = self.client.post(self.list_url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("category", response.data)
        self.assertIn("name", response.data)
        self.assertIn("price", response.data)

    def test_create_product_missing_category(self):
        payload = {
            "name": "Smartphone Without Category",
            "price": "699.99",
            "stock_quantity": 25,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_invalid_category_id(self):
        payload = {
            "category": 99999,
            "name": "Smartphone Bad Cat",
            "price": "699.99",
            "stock_quantity": 25,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("category", response.data)

    def test_create_product_invalid_price(self):
        payload = {
            "category": self.category.id,
            "name": "Bad Price Product",
            "price": "not-a-number",
            "stock_quantity": 5,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)

    def test_create_product_negative_stock(self):
        payload = {
            "category": self.category.id,
            "name": "Negative Stock Product",
            "price": "50.00",
            "stock_quantity": -10,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("stock_quantity", response.data)

    def test_retrieve_product(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Laptop")
        self.assertEqual(response.data["category_name"], "Electronics")

    def test_retrieve_invalid_product_id_returns_404(self):
        response = self.client.get(self.invalid_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)

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

    def test_partial_update_product_patch(self):
        payload = {"price": "1150.00"}
        response = self.client.patch(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.price, Decimal("1150.00"))
        self.assertEqual(self.product.name, "Laptop")

    def test_update_invalid_product_id_returns_404(self):
        payload = {"category": self.category.id, "name": "Non-existent", "price": "100.00"}
        response = self.client.put(self.invalid_detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_delete_invalid_product_id_returns_404(self):
        response = self.client.delete(self.invalid_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
