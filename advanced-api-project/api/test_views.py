from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

def setUp(self):
    self.user = User.objects.create_user(username='testuser', password='pass')
    self.client = APIClient()
    self.client.force_authenticate(user=self.user)

class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user and log in
        self.user = User.objects.create_user(username='testuser', password='pass123')
        logged_in = self.client.login(username='testuser', password='pass123')
        assert logged_in, "Login failed in test setup"

        # Sample book and URLs
        self.book = Book.objects.create(
            title="Test Book",
            author="Yonatan",
            published_date="2024-01-01"
        )
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', args=[self.book.id])
        self.create_url = reverse('book-create')
        self.update_url = reverse('book-update', args=[self.book.id])
        self.delete_url = reverse('book-delete', args=[self.book.id])


    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Yonatan",
            published_date="2024-01-01"
        )
        self.list_url = reverse('book-list')
        self.detail_url = reverse('book-detail', args=[self.book.id])
        self.create_url = reverse('book-create')
        self.update_url = reverse('book-update', args=[self.book.id])
        self.delete_url = reverse('book-delete', args=[self.book.id])

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Test Book", str(response.data))

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Book")

    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": "Yonatan",
            "published_date": "2025-01-01"
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)

    def test_update_book(self):
        data = {
            "title": "Updated Book",
            "author": "Yonatan",
            "published_date": "2024-01-01"
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)