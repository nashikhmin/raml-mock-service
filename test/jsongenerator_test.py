import json
import unittest

from server.jsongenerator.jsongenerator import JsonGenerator


class MyTestCase(unittest.TestCase):
    def test_number(self):
        schema = '{ "type": "number" }'
        generator = JsonGenerator(schema)
        out = generator.get_node(json.loads(schema))
        self.assertIsInstance(out, int, str(out) + ' is not number')

    def test_string(self):
        schema = '{ "type": "string" }'
        generator = JsonGenerator(schema)
        out = generator.get_node(json.loads(schema))
        self.assertIsInstance(out, str, str(out) + ' is not string')

    def test_string(self):
        schema = '{ "type": "string" }'
        generator = JsonGenerator(schema)
        out = generator.get_node(json.loads(schema))
        self.assertIsInstance(out, str, str(out) + ' is not string')

    def test_enum(self):
        schema = '{"enum": ["red", "amber", "green", null, 42]}'
        array = json.loads('["red", "amber", "green", null, 42]')
        generator = JsonGenerator(schema)
        out = generator.get_node(json.loads(schema))
        self.assertIn(out, array, str(out) + ' is not in ' + str(array))

    def test_string_max(self):
        schema = '{"type": "string","maxLength": 3}'
        generator = JsonGenerator(schema)
        out = generator.get_node(json.loads(schema))
        self.assertLessEqual(len(out), 3, 'len of ' + str(out) + ' is more than maxLength')

    def test_string_min(self):
        schema = '{"type": "string","minLength": 10}'
        generator = JsonGenerator(schema)
        out = generator.get_node(json.loads(schema))
        self.assertGreaterEqual(len(out), 10, 'len of ' + str(out) + ' is less than minLength')

    def test_string_regular(self):
        pattern_json = '^(\\\\([0-9]{3}\\\\))?[0-9]{3}-[0-9]{4}$'
        pattern_native = '^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$'
        schema = '{"type": "string", "pattern": "' + pattern_json + '"}'
        generator = JsonGenerator(schema)
        out = generator.get_node(json.loads(schema))
        self.assertRegex(out, pattern_native)

    def test_multitype(self):
        schema = '{ "type": ["number", "string"] }'
        generator = JsonGenerator(schema)
        out = generator.get_node(json.loads(schema))
        if not isinstance(out, int) and not isinstance(out, str):
            self.fail(str(out) + ' is not number or string type')


if __name__ == '__main__':
    unittest.main()
