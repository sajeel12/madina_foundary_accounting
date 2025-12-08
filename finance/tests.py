from django.test import TestCase, Client
from django.urls import reverse
from .models import Transaction, Category
from django.utils import timezone

class FinanceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test Category", type="IN")
        self.transaction = Transaction.objects.create(
            type="IN",
            amount=100.00,
            date=timezone.now().date(),
            description="Test Transaction",
            category=self.category
        )

    def test_model_creation(self):
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(str(self.transaction), f"Cash In: 100.00 on {self.transaction.date}")

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Transaction")
        self.assertContains(response, "100.0")

    def test_reports_view(self):
        response = self.client.get(reverse('reports'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Financial Reports")

    def test_transaction_create_view(self):
        response = self.client.get(reverse('transaction_create'))
        self.assertEqual(response.status_code, 200)
