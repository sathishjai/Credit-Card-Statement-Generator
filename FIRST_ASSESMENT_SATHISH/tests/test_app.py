import unittest
import sys
import os
import datetime
from decimal import Decimal

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app, get_db_connection, fetch_customer_info, fetch_statements, fetch_transactions, generate_pdf, tr

class TestCIMBStatementGenerator(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()
        
        # Test data
        self.test_customer = (1, "John Doe", "123 Test St\nTest City\n12345", 
                            "4111-1111-1111-1111", "80-0024165-6", 
                            Decimal('25000.00'), Decimal('15000.00'))
        
        self.test_statement = (1, 1, datetime.date(2024, 1, 1),
                             datetime.date(2024, 1, 1), datetime.date(2024, 1, 31),
                             Decimal('1000.00'), Decimal('50.00'),
                             datetime.date(2024, 2, 15), 1000)
        
        self.test_transactions = [
            (datetime.date(2024, 1, 15), "Test Purchase", Decimal('-100.00'), "Purchase"),
            (datetime.date(2024, 1, 20), "Test Payment", Decimal('500.00'), "Payment")
        ]

    def test_database_connection(self):
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        conn.close()

    def test_customer_fetch(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Test fetch by ID
        result = fetch_customer_info(cursor, customer_id=1)
        self.assertIsNotNone(result)
        
        # Test fetch by name
        result = fetch_customer_info(cursor, customer_name="John")
        self.assertIsNotNone(result)
        
        conn.close()

    def test_statement_fetch(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        result = fetch_statements(cursor, customer_id=1)
        self.assertIsNotNone(result)
        conn.close()

    def test_transaction_fetch(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        result = fetch_transactions(cursor, statement_id=1)
        self.assertIsNotNone(result)
        conn.close()

    def test_pdf_generation(self):
        # Test PDF generation for different languages
        for lang in ['en', 'ms', 'vi', 'tl', 'en-gb', 'th']:
            filename = generate_pdf(self.test_customer, self.test_statement, 
                                 self.test_transactions, lang=lang)
            self.assertIsNotNone(filename)
            self.assertTrue(os.path.exists(filename))
            
            # Test page borders
            with open(filename, 'rb') as pdf_file:
                from PyPDF2 import PdfReader
                reader = PdfReader(pdf_file)
                for page in reader.pages:
                    # Check if page has content (borders should be part of content)
                    self.assertIsNotNone(page.get_contents())
                    # Check if page has correct dimensions for borders
                    mediabox = page.mediabox
                    self.assertAlmostEqual(float(mediabox.width), 595.28, places=1)  # A4 width in points
                    self.assertAlmostEqual(float(mediabox.height), 841.89, places=1)  # A4 height in points

    def test_translations(self):
        # Test key translations
        test_keys = ['STATEMENT DATE', 'ACCOUNT SUMMARY', 'TRANSACTION DETAILS']
        for lang in ['en', 'ms', 'vi', 'tl', 'en-gb', 'th']:
            for key in test_keys:
                result = tr(key, lang)
                self.assertIsNotNone(result)
                self.assertNotEqual(result, '')

    def test_web_routes(self):
        # Test index page
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Test search functionality
        response = self.app.post('/search', data={
            'language': 'en',
            'search_type': 'id',
            'search_value': '1'
        })
        self.assertEqual(response.status_code, 200)

    def test_error_handling(self):
        # Test invalid customer ID
        response = self.app.post('/search', data={
            'language': 'en',
            'search_type': 'id',
            'search_value': '999999'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on error

if __name__ == '__main__':
    unittest.main()