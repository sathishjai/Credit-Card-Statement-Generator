import unittest
import sys
import os
import datetime
import tempfile
import shutil
from decimal import Decimal
from unittest.mock import patch, MagicMock

# Add parent directory to path to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app, get_db_connection, fetch_customer_info, fetch_statements, fetch_transactions, generate_pdf, tr, log_error, download_fonts, FONT_MAPPING

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
        
        # Create temporary directories for testing
        self.test_dir = tempfile.mkdtemp()
        self.original_pdfs_dir = "pdfs"
        self.original_logs_dir = "logs"
        
        # Ensure test directories exist
        os.makedirs(os.path.join(self.test_dir, "pdfs"), exist_ok=True)
        os.makedirs(os.path.join(self.test_dir, "logs"), exist_ok=True)

    def tearDown(self):
        # Clean up temporary test directory
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_database_connection(self):
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        conn.close()
        
    def test_database_connection_error(self):
        # Test with invalid connection parameters
        with patch('app.pymysql.connect', side_effect=Exception("Connection error")):
            conn = get_db_connection()
            self.assertIsNone(conn)

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
        
    def test_customer_fetch_validation(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Test with invalid ID (non-numeric)
        result = fetch_customer_info(cursor, customer_id="abc")
        self.assertIsNone(result)
        
        # Test with invalid name (too short)
        result = fetch_customer_info(cursor, customer_name="a")
        self.assertIsNone(result)
        
        # Test with no parameters
        result = fetch_customer_info(cursor)
        self.assertIsNone(result)
        
        conn.close()
        
    def test_customer_fetch_error(self):
        # Mock cursor to simulate database error
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("Database error")
        
        # Test error handling
        result = fetch_customer_info(mock_cursor, customer_id=1)
        self.assertIsNone(result)

    def test_statement_fetch(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        result = fetch_statements(cursor, customer_id=1)
        self.assertIsNotNone(result)
        conn.close()
        
    def test_statement_fetch_error(self):
        # Mock cursor to simulate database error
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("Database error")
        
        # Test error handling
        result = fetch_statements(mock_cursor, customer_id=1)
        self.assertIsNone(result)

    def test_transaction_fetch(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        result = fetch_transactions(cursor, statement_id=1)
        self.assertIsNotNone(result)
        conn.close()
        
    def test_transaction_fetch_error(self):
        # Mock cursor to simulate database error
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = Exception("Database error")
        
        # Test error handling
        result = fetch_transactions(mock_cursor, statement_id=1)
        self.assertIsNone(result)

    def test_pdf_generation(self):
        # Test PDF generation for different languages
        for lang in ['en', 'ms', 'vi', 'tl', 'en-gb', 'th', 'ta']:
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

    def test_pdf_generation_with_invalid_data(self):
        # Test with invalid numeric values
        invalid_customer = (1, "John Doe", "123 Test St\nTest City\n12345", 
                          "4111-1111-1111-1111", "80-0024165-6", 
                          "invalid", "invalid")
        
        invalid_statement = (1, 1, datetime.date(2024, 1, 1),
                           datetime.date(2024, 1, 1), datetime.date(2024, 1, 31),
                           "invalid", "invalid",
                           datetime.date(2024, 2, 15), "invalid")
        
        # Should handle invalid data gracefully
        filename = generate_pdf(invalid_customer, invalid_statement, self.test_transactions)
        self.assertIsNotNone(filename)
        self.assertTrue(os.path.exists(filename))
        
    def test_pdf_generation_with_missing_fonts(self):
        # Test PDF generation with missing fonts
        with patch('os.path.exists', return_value=False):
            filename = generate_pdf(self.test_customer, self.test_statement, 
                                 self.test_transactions)
            self.assertIsNone(filename)
            
    def test_pdf_generation_error(self):
        # Test error handling in PDF generation
        with patch('app.FPDF', side_effect=Exception("PDF error")):
            filename = generate_pdf(self.test_customer, self.test_statement, 
                                 self.test_transactions)
            self.assertIsNone(filename)

    def test_translations(self):
        # Test key translations
        test_keys = ['STATEMENT DATE', 'ACCOUNT SUMMARY', 'TRANSACTION DETAILS']
        for lang in ['en', 'ms', 'vi', 'tl', 'en-gb', 'th', 'ta']:
            for key in test_keys:
                result = tr(key, lang)
                self.assertIsNotNone(result)
                self.assertNotEqual(result, '')
                
        # Test fallback to English for unknown language
        result = tr('STATEMENT DATE', 'unknown_lang')
        self.assertEqual(result, 'STATEMENT DATE')
        
        # Test fallback for unknown key
        result = tr('UNKNOWN_KEY', 'en')
        self.assertEqual(result, 'UNKNOWN_KEY')

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
        
        # Test statements route
        response = self.app.get('/statements/1/en')
        self.assertEqual(response.status_code, 200)
        
        # Test view_customers route
        response = self.app.get('/view_customers')
        self.assertEqual(response.status_code, 200)
        
        # Test download route
        # Create a dummy PDF file for testing
        with open("pdfs/test.pdf", "w") as f:
            f.write("Test PDF content")
        response = self.app.get('/download/test.pdf')
        self.assertEqual(response.status_code, 200)

    def test_error_handling(self):
        # Test invalid customer ID
        response = self.app.post('/search', data={
            'language': 'en',
            'search_type': 'id',
            'search_value': '999999'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on error
        
        # Test empty search value
        response = self.app.post('/search', data={
            'language': 'en',
            'search_type': 'id',
            'search_value': ''
        })
        self.assertEqual(response.status_code, 302)  # Redirect on error
        
        # Test non-numeric ID
        response = self.app.post('/search', data={
            'language': 'en',
            'search_type': 'id',
            'search_value': 'abc'
        })
        self.assertEqual(response.status_code, 302)  # Redirect on error
        
        # Test invalid statement ID
        response = self.app.get('/generate/1/999/en')
        self.assertEqual(response.status_code, 302)  # Redirect on error
        
        # Test invalid customer ID in statements route
        response = self.app.get('/statements/999/en')
        self.assertEqual(response.status_code, 302)  # Redirect on error

    def test_log_error(self):
        # Test error logging functionality
        test_message = "Test error message"
        with patch('builtins.open', create=True) as mock_open:
            log_error(test_message)
            mock_open.assert_called_once()
            
    def test_download_fonts(self):
        # Test font download functionality
        with patch('urllib.request.urlretrieve') as mock_urlretrieve:
            with patch('os.path.exists', return_value=False):
                download_fonts()
                # Should attempt to download all fonts
                self.assertGreaterEqual(mock_urlretrieve.call_count, len(FONT_MAPPING))
                
    def test_font_mapping(self):
        # Test font mapping for all supported languages
        for lang, font_file in FONT_MAPPING.items():
            self.assertIsNotNone(font_file)
            self.assertTrue(isinstance(font_file, str))
            
    def test_health_check_route(self):
        # Test health check endpoint
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
    def test_test_pdf_route(self):
        # Test the test_pdf route
        response = self.app.get('/test_pdf')
        self.assertEqual(response.status_code, 302)  # Should redirect to download

if __name__ == '__main__':
    unittest.main()