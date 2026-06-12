import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "output" / "compliance_status.json"

class TestOutputSchema(unittest.TestCase):
    def test_compliance_status_schema_exists(self):
        self.assertTrue(OUTPUT.exists(), f"Expected output file at {OUTPUT}")

    def test_compliance_status_schema_fields(self):
        with open(OUTPUT, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Top-level fields
        expected_keys = {"timestamp","student_id","student_name","alert_flag","violation_level","violations","conflicts","remediation_actions","recommendation"}
        self.assertTrue(set(data.keys()).issuperset(expected_keys))

        # Types
        self.assertIsInstance(data["timestamp"], str)
        self.assertIsInstance(data["student_id"], str)
        self.assertIsInstance(data["student_name"], str)
        self.assertIsInstance(data["alert_flag"], bool)
        self.assertIsInstance(data["violation_level"], str)
        self.assertIsInstance(data["violations"], list)
        self.assertIsInstance(data["conflicts"], list)
        self.assertIsInstance(data["remediation_actions"], list)
        self.assertIsInstance(data["recommendation"], str)

        # If there are violations, check structure of first violation
        if data["violations"]:
            v = data["violations"][0]
            self.assertIn("type", v)
            self.assertIn("severity", v)

        # If there are conflicts, check structure of first conflict
        if data["conflicts"]:
            c = data["conflicts"][0]
            self.assertIn("type", c)
            self.assertIn("severity", c)
            self.assertIn("exam_date", c)

if __name__ == '__main__':
    unittest.main()
