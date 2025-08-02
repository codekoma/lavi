import unittest
from src.main import sanitize_user_inputs

class TestSanitizeUserInputs(unittest.TestCase):
    def test_basic_threats(self):
        inputs = [
            "<script>alert('x')</script>",
            "' OR 1=1 --",
            "rm -rf / ; echo 'hacked'"
        ]
        result = sanitize_user_inputs(inputs)
        self.assertEqual(len(result["cleaned_inputs"]), 3)
        self.assertGreaterEqual(result["threats_detected"].get("xss", 0), 1)
        self.assertGreaterEqual(result["threats_detected"].get("sqli", 0), 1)
        self.assertGreaterEqual(result["threats_detected"].get("cmd_injection", 0), 1)

    def test_unicode_and_sanitization(self):
        inputs = ["<scrípt>évìl()</scrípt>", "SELECT * FROM users"]
        result = sanitize_user_inputs(inputs)
        for out in result["cleaned_inputs"]:
            self.assertNotIn("<", out)
            self.assertNotIn(">", out)
        self.assertEqual(result["threats_detected"].get("xss", 0), 1)
        self.assertEqual(result["threats_detected"].get("sqli", 0), 1)

if __name__ == "__main__":
    unittest.main()
