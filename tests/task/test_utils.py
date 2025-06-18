from django.test import TestCase
from rest_framework.exceptions import ValidationError
from task.utils import is_int_or_valid_error


class TaskUtilsTestCase(TestCase):

    TWO_STR = "2"
    TWO_INT = 2

    SOME_STR = "some str"
    
    @classmethod
    def setUpTestData(cls):
        pass

    def test_is_int_or_valid_error_input_str_num(self):
        result = is_int_or_valid_error(num_check=self.TWO_STR)

        self.assertEqual(type(result), int)
        self.assertEqual(result, self.TWO_INT)

    def test_is_int_or_valid_error_input_int_num(self):
        result = is_int_or_valid_error(num_check=self.TWO_INT)

        self.assertEqual(type(result), int)
        self.assertEqual(result, self.TWO_INT)
    
    def test_is_int_or_valid_error_input_str_str(self):
        with self.assertRaises(ValidationError):
            is_int_or_valid_error(num_check=self.SOME_STR)