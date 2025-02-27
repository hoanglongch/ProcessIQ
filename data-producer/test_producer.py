#!/usr/bin/env python3
import unittest
from producer import generate_fake_metric

class TestProducer(unittest.TestCase):
    def test_generate_fake_metric(self):
        metric = generate_fake_metric()
        self.assertIn("sensor_id", metric)
        self.assertIn("temperature", metric)
        self.assertIn("pressure", metric)
        self.assertIn("timestamp", metric)

        self.assertIsInstance(metric["sensor_id"], str)
        self.assertIsInstance(metric["temperature"], float)
        self.assertIsInstance(metric["pressure"], float)
        self.assertIsInstance(metric["timestamp"], int)

if __name__ == "__main__":
    unittest.main()