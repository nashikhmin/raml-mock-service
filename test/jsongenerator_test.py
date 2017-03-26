import json
import unittest

from server.jsongenerator.jsongenerator import JsonGenerator


class CommonGeneratorTestCase(unittest.TestCase):
    def test_enum(self):
        schema = '{"enum": ["red", "amber", "green", null, 42]}'
        array = json.loads('["red", "amber", "green", null, 42]')
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        self.assertIn(out, array, str(out) + ' is not in ' + str(array))

    def test_multitype(self):
        schema = '{ "type": ["number", "string"] }'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        if not isinstance(out, float) and not isinstance(out, str):
            self.fail(str(out) + ' is not number or string type')


class StringGeneratorTestCase(unittest.TestCase):
    def test_string(self):
        schema = '{ "type": "string" }'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        self.assertIsInstance(out, str, str(out) + ' is not string')

    def test_string_max(self):
        schema = '{"type": "string","maxLength": 3}'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        self.assertLessEqual(len(out), 3, 'len of ' + str(out) + ' is more than maxLength')

    def test_string_min(self):
        schema = '{"type": "string","minLength": 10}'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        self.assertGreaterEqual(len(out), 10, 'len of ' + str(out) + ' is less than minLength')

    def test_string_regular(self):
        pattern_json = '^(\\\\([0-9]{3}\\\\))?[0-9]{3}-[0-9]{4}$'
        pattern_native = '^(\\([0-9]{3}\\))?[0-9]{3}-[0-9]{4}$'
        schema = '{"type": "string", "pattern": "' + pattern_json + '"}'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        self.assertRegex(out, pattern_native)


class NumberGeneratorTestCase(unittest.TestCase):
    def test_number(self):
        schema = '{ "type": "number" }'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        self.assertIsInstance(out, float, str(out) + ' is not number')

    def test_number_multiple_of(self):
        schema = '{ "type": "number","multipleOf" : 3.4 }'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        self.assertAlmostEqual(float(out) / 3.4, int(out / 3.4), str(out) + ' is not multipleOf 3.4', 1e-7)

    def test_number_min(self):
        schema = '{ "type": "number", "minimum": 20}'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        self.assertGreaterEqual(out, 20)

    def test_number_max(self):
        schema = '{ "type": "number", "maximum": -15}'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        self.assertLessEqual(out, -15, )

    def test_number_exlusive_min(self):
        schema = '{ "type": "number", "multipleOf" : 1.0, "minimum": 1, "maximum": 2,"exclusiveMinimum": true}'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        self.assertGreater(out, 1)

    def test_number_exlusive_max(self):
        schema = '{ "type": "number", "multipleOf" : 1.0, "minimum": 1, "maximum": 2,"exclusiveMaximum": true}'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        self.assertLess(out, 2)


class ObjectGeneratorTestCase(unittest.TestCase):
    def test_object_clean(self):
        schema = '{ "type": "object" }'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        if not isinstance(out, dict):
            self.fail(str(out) + ' is not object')

    def test_object_properties(self):
        schema = '{"type": "object", "properties": {"number":{ "type": "number" }}}'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        self.assertEqual(out.keys(), {'number': 12}.keys(), 'there are not properties')

    def test_object_min(self):
        schema = '{"type": "object","minProperties": 5}'
        generator = JsonGenerator(schema)
        out = generator._get_node(json.loads(schema))
        self.assertGreaterEqual(len(out.keys()), 2, 'number of properties of ' + str(out) + ' is less than minLength')


if __name__ == '__main__':
    unittest.main()
