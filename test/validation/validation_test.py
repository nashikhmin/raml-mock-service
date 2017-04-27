import unittest

import ramlfications

from common import message
from server.validator import Validator

"""
Tests for module of the program -
requests parameters validator
"""
RAML_FILE = "resource/validate.raml"
parser = ramlfications.parse(RAML_FILE)


class TestCommon(unittest.TestCase):
    def _test_raise_exception(self, args, msg):
        with self.assertRaises(Exception) as context:
            self.validator.validate_required_components(args)
        self.assertEquals(msg, str(context.exception))

    def _test_not_raise_exception(self, args, msg):
        try:
            self.validator.validate_required_components(args)
        except Exception:
            self.fail(msg)

    def setUp(self):
        params = parser.resources[3].query_params
        self.validator = Validator(params)

    def test_required(self):
        arguments1 = {'a': 1, 'b': 2}
        self._test_not_raise_exception(arguments1, message.ERR_REQUIRED_ARGUMENT)

        arguments2 = {'a': 1, 'b': 2, 'd': 4}
        self._test_not_raise_exception(arguments2, message.ERR_REQUIRED_ARGUMENT)

        arguments3 = {'b': 2}
        self._test_raise_exception(arguments3, message.ERR_REQUIRED_ARGUMENT)

        arguments3 = {'d': 2, 'f': 5}
        self._test_raise_exception(arguments3, message.ERR_REQUIRED_ARGUMENT)


class TestStringType(unittest.TestCase):
    def _test_raise_exception(self, value, param, msg):
        with self.assertRaises(Exception) as context:
            self.validator.validate_string(value, param)
        self.assertEquals(msg, str(context.exception))

    def _test_not_raise_exception(self, value, param, msg):
        try:
            self.validator.validate_string(value, param)
        except Exception:
            self.fail(msg)

    def setUp(self):
        params = parser.resources[0].query_params
        self.validator = Validator(params)

    def test_min(self):
        param = self.validator.get_template_argument('min')
        self._test_raise_exception('a', param, message.ERR_STRING_MIN)
        self._test_not_raise_exception('aaa', param, message.ERR_STRING_MIN)

    def test_max(self):
        param = self.validator.get_template_argument('max')
        self._test_raise_exception('a' * 10, param, message.ERR_STRING_MAX)
        self._test_not_raise_exception('a' * 3, param, message.ERR_STRING_MAX)

    def test_enum(self):
        param = self.validator.get_template_argument('enum')
        self._test_raise_exception('a', param, message.ERR_STRING_ENUM)
        self._test_not_raise_exception('aaa', param, message.ERR_STRING_ENUM)


class TestNumberType(unittest.TestCase):
    def _test_raise_exception(self, value, param, msg):
        with self.assertRaises(Exception) as context:
            self.validator.validate_number(value, param)
        self.assertEquals(msg, str(context.exception))

    def _test_not_raise_exception(self, value, param, msg):
        try:
            self.validator.validate_number(value, param)
        except Exception:
            self.fail(msg)

    def setUp(self):
        params = parser.resources[1].query_params
        self.validator = Validator(params)

    def test_min(self):
        param = self.validator.get_template_argument('min')
        self._test_raise_exception(-1.4353, param, message.ERR_MINIMUM)
        self._test_not_raise_exception(0.213, param, message.ERR_MINIMUM)

    def test_max(self):
        param = self.validator.get_template_argument('max')
        self._test_raise_exception(11, param, message.ERR_MAXIMUM)
        self._test_not_raise_exception(10, param, message.ERR_MAXIMUM)

    def test_num(self):
        param = self.validator.get_template_argument('number')
        self._test_raise_exception('a', param, message.ERR_NUMBER)
        self._test_not_raise_exception(10.342, param, message.ERR_NUMBER)


class TestIntegerMethods(unittest.TestCase):
    def _test_raise_exception(self, value, param, msg):
        with self.assertRaises(Exception) as context:
            self.validator.validate_integer(value, param)
        self.assertEquals(msg, str(context.exception))

    def _test_not_raise_exception(self, value, param, msg):
        try:
            self.validator.validate_integer(value, param)
        except Exception:
            self.fail(msg)

    def setUp(self):
        params = parser.resources[2].query_params
        self.validator = Validator(params)

    def test_min(self):
        param = self.validator.get_template_argument('min')
        self._test_raise_exception(-1, param, message.ERR_MINIMUM)
        self._test_not_raise_exception(0, param, message.ERR_MINIMUM)

    def test_max(self):
        param = self.validator.get_template_argument('max')
        self._test_raise_exception(11, param, message.ERR_MAXIMUM)
        self._test_not_raise_exception(10, param, message.ERR_MAXIMUM)

    def test_integer(self):
        param = self.validator.get_template_argument('integer')
        self._test_raise_exception('a', param, message.ERR_INTEGER)
        self._test_not_raise_exception(5, param, message.ERR_INTEGER)


if __name__ == '__main__':
    unittest.main()