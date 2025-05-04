import os
import json
import unittest
from datetime import datetime
from logger import log_event, LOG_DIR

class TestLogger(unittest.TestCase):
    def setUp(self):
        # Ensure log directory exists and track created log files.
        os.makedirs(LOG_DIR, exist_ok=True)
        self.created_logs = []

    def tearDown(self):
        # Clean up created log files after each test.
        for log_file in self.created_logs:
            if os.path.exists(log_file):
                os.remove(log_file)

    def test_log_event_creates_file_and_returns_correct_path(self):
        category = "test"
        data = {"message": "This is a test log"}
        log_file = log_event(category, data)
        self.created_logs.append(log_file)

        # Check that the file was created
        self.assertTrue(os.path.exists(log_file))

        # Read the JSON content
        with open(log_file, "r") as f:
            content = json.load(f)

        # Check that the file content contains the expected keys and values
        self.assertIn("timestamp", content)
        self.assertIn("category", content)
        self.assertIn("data", content)
        self.assertEqual(content["category"], category)
        self.assertEqual(content["data"], data)

        # Validate timestamp format. Expected format: "YYYY-MM-DD_HH-MM-SS"
        try:
            datetime.strptime(content["timestamp"], "%Y-%m-%d_%H-%M-%S")
        except ValueError:
            self.fail("Timestamp format is incorrect.")

    def test_log_file_naming(self):
        category = "naming"
        data = {"info": "Test naming convention"}
        log_file = log_event(category, data)
        self.created_logs.append(log_file)

        # The log file name should start with the category and have a timestamp.
        basename = os.path.basename(log_file)
        self.assertTrue(basename.startswith(category + "_"))
        self.assertTrue(basename.endswith(".json"))

if __name__ == "__main__":
    unittest.main()