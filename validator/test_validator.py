#!/usr/bin/env python3
import unittest
from main import validate_metric

class TestValidator(unittest.TestCase):
    def test_valid_metric(self):
        metric = {
            "sensor_id": "sensor-1",
            "temperature": 500,
            "pressure": 2500
        }
        self.assertTrue(validate_metric(metric))

    def test_invalid_temp(self):
        metric = {
            "sensor_id": "sensor-1",
            "temperature": 1500,  # out of range
            "pressure": 2500
        }
        self.assertFalse(validate_metric(metric))

    def test_missing_fields(self):
        metric = {"sensor_id": "sensor-1"}
        self.assertFalse(validate_metric(metric))

if __name__ == "__main__":
    unittest.main()