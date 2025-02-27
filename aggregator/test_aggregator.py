#!/usr/bin/env python3
import unittest
from fastapi.testclient import TestClient
from aggregator import app

class TestAggregator(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.auth = ("admin", "secret")  # matches aggregator's hard-coded credentials

    def test_health_check(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_metrics_summary_unauthorized(self):
        # Try without auth
        response = self.client.get("/metrics/summary")
        self.assertEqual(response.status_code, 401)

    def test_metrics_summary_authorized(self):
        # Use basic auth
        response = self.client.get("/metrics/summary", auth=self.auth)
        self.assertEqual(response.status_code, 200)
        # The exact structure depends on DB data; just confirm we get a JSON list
        self.assertIsInstance(response.json(), list)

if __name__ == "__main__":
    unittest.main()