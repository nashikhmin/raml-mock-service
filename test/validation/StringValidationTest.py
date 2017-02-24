import unittest

from validator import Validator


class StringValidationTest(unittest.TestCase):
    def test_something(self):
        validator = Validator()
        validator.validate_string("a")


if __name__ == '__main__':
    unittest.main()
