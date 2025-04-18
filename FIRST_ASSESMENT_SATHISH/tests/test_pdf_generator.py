import unittest
from app import generate_pdf, tr
import os
import datetime

class TestPDFGenerator(unittest.TestCase):
    def setUp(self):
        self.test_customer = (1, "Test User", "123 Test St\nTest City\n12345", 
                            "4444-3333-2222-1111", "ACC123456", 25000.00, 16000.00)
        self.test_statement = (1, 1, datetime.date(2025, 4, 10), 
                             datetime.date(2025, 3, 11), datetime.date(2025, 4, 10),
                             5000.00, 250.00, datetime.date(2025, 5, 1), 1000)
        self.test_transactions = [
            (datetime.date(2025, 3, 15), "Test Purchase", -100.00, "Purchase"),
            (datetime.date(2025, 3, 20), "Test Payment", 500.00, "Payment")
        ]

    def test_pdf_generation(self):
        filename = generate_pdf(self.test_customer, self.test_statement, 
                              self.test_transactions)
        self.assertIsNotNone(filename)
        self.assertTrue(os.path.exists(filename))
        
    def test_translations(self):
        self.assertEqual(tr("STATEMENT DATE", "en"), "STATEMENT DATE")
        self.assertEqual(tr("STATEMENT DATE", "ms"), "TARIKH PENYATA")

if __name__ == '__main__':
    unittest.main()