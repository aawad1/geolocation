from django.test import TestCase
from .views import validate_input

error_message = "Invalid input. Please enter valid coordinates or location name."

class ValidateInputTestCase(TestCase):
    def test_valid_coordinates(self):
        input_str = "42.123,-71.456"
        result = validate_input(input_str)
        self.assertEqual(result, [42.123, -71.456])

    def test_invalid_coordinates(self):
        input_str = "1000,2000"  # Invalid coordinates
        result = validate_input(input_str)
        self.assertIsNone(result)
        self.assertEqual(error_message, "Invalid input. Please enter valid coordinates or location name.")

    def test_invalid_input_format(self):
        input_str = "42.123,-71.456,100"  # Invalid input format
        result = validate_input(input_str)
        self.assertIsNone(result)
        self.assertEqual(error_message, "Invalid input. Please enter valid coordinates or location name.")
