import unittest

import ramlfications

from common import message
from validator import Validator


class TestStringMethods(unittest.TestCase):
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
        RAML_FILE = "resource/validate.raml"
        parser = ramlfications.parse(RAML_FILE)
        params = parser.resources[0].query_params
        self.validator = Validator(params)


    def test_min(self):
        param = self.validator.get_template_argument('min')
        self._test_raise_exception('a', param, message.ERR_STRING_MIN)
        self._test_not_raise_exception('aaa', param, message.ERR_STRING_MIN)

    def test_max(self):
        param = self.validator.get_template_argument('max')
        self._test_raise_exception('a'*10, param, message.ERR_STRING_MAX)
        self._test_not_raise_exception('a'*3, param, message.ERR_STRING_MAX)


    def test_enum(self):
        param = self.validator.get_template_argument('enum')
        self._test_raise_exception('a' , param, message.ERR_STRING_ENUM)
        self._test_not_raise_exception('aaa', param, message.ERR_STRING_ENUM)

if __name__ == '__main__':
    unittest.main()