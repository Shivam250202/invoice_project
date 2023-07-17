from django.test import TestCase
from rest_framework.test import APIClient
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_invoice(self):
        payload = {
            'date': '2023-07-17',
            'invoice_no': 'INV-001',
            'customer_name': 'John Doe',
            'details': [
                {
                    'description': 'Item 1',
                    'quantity': 2,
                    'unit_price': 10.00,
                    'price': 20.00
                },
                {
                    'description': 'Item 2',
                    'quantity': 1,
                    'unit_price': 5.00,
                    'price': 5.00
                }
            ]
        }

        response = self.client.post('/api/invoices/', payload, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(InvoiceDetail.objects.count(), 2)

        invoice = Invoice.objects.first()
        self.assertEqual(invoice.date.strftime('%Y-%m-%d'), '2023-07-17')
        self.assertEqual(invoice.invoice_no, 'INV-001')
        self.assertEqual(invoice.customer_name, 'John Doe')

        detail1 = InvoiceDetail.objects.get(invoice=invoice, description='Item 1')
        self.assertEqual(detail1.quantity, 2)
        self.assertEqual(detail1.unit_price, 10.00)
        self.assertEqual(detail1.price, 20.00)

        detail2 = InvoiceDetail.objects.get(invoice=invoice, description='Item 2')
        self.assertEqual(detail2.quantity, 1)
        self.assertEqual(detail2.unit_price, 5.00)
        self.assertEqual(detail2.price, 5.00)

