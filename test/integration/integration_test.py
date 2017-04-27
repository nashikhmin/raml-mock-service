"""
Integration tests that validate behaviour of all program
"""
import unittest

import patch as patch
import ramlfications
import sys

import main
RAML_FILE = "resource/validate.raml"
parser = ramlfications.parse(RAML_FILE)


class TestCommon(unittest.TestCase):


    def test_start(self):
        file = './test/resource/example.raml'
        testargs = ["prog", "-f", "/home/fenton/project/setup.py"]
        with patch.object(sys, 'argv', testargs):
            setup = get_setup_file()
            assert setup == "/home/fenton/project/setup.py"

