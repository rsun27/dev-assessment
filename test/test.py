import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch
from app.main import app
from test_cases import *

class RefundTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_valid_pin(self):
        response = self.client.post("/refund", json=valid_payload)

        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        self.assertIn("pin", data)
        self.assertIn("yearsEligible", data)
        self.assertIn("totalRefund", data)

        # Type checks
        self.assertIsInstance(data["pin"], str)
        self.assertIsInstance(data["yearsEligible"], int)
        self.assertIsInstance(data["totalRefund"], float)

    def test_pin_returns_empty_data(self):
        """Test that a PIN not in the external API returns a 404 with error"""
        response = self.client.post("/refund", json=invalid_payload)

        self.assertIn(response.status_code, [404, 400])
        data = response.get_json()
        self.assertIn("error", data)
        self.assertTrue("no comparables" in data["error"].lower())
    
        
    @patch("app.main.compound_interest", new=compound_interest)
    @patch("app.main.requests.get")
    def test_expected_refund_output(self, mock_get): 
        # Mock requests.get().json()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = test_case_response_1

        response = self.client.post("/refund", json=valid_payload)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()

        # Assert: Exact expected output
        self.assertEqual(data["pin"], "26062070090000")
        self.assertEqual(data["yearsEligible"], 4)
        self.assertAlmostEqual(data["totalRefund"], 7043.40, places=2)

    @patch("app.main.compound_interest", new=compound_interest)
    @patch("app.main.requests.get")
    def test_property_below_average_gets_no_refund(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = test_case_response_2

        response = self.client.post("/refund", json={"pin": "1234567890"})
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertEqual(data["pin"], "1234567890")
        self.assertEqual(data["yearsEligible"], 0)  
        self.assertAlmostEqual(data["totalRefund"], 0.00, places=2)


if __name__ == '__main__':
    unittest.main()