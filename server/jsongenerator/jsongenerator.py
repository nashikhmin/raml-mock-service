import json

import rstr as rstr

import server.jsongenerator.utils as utils


# This class generate valid Json based on Json Schema
class JsonGenerator:
    # array constants
    _array_min_count = 4
    _array_max_count = 10
    # string constants
    _default_len_min_string = 3
    _default_len_max_string = 26
    # number constants
    _default_min_number = -1e9
    _default_max_number = 1e9
    _exclisuve_delta = 1e-5

    def __init__(self, schema):
        self.data = json.loads(schema)

        self._types = {
            'object': self._get_object,
            'string': self._get_string,
            'array': self.get_array,
            'number': self._get_number,
        }

    def getJson(self):
        return self._get_node(self.data)

    def _get_node(self, node):
        # TODO: improve and delete this statement
        if 'type' not in node:
            return None
        type = node['type']

        if "enum" in node:
            enum = node["enum"]
            i = utils.generate_int(0, len(enum) - 1)
            return enum[i]

        if isinstance(type, list):
            return self._types[type[0]](node)
        return self._types[type](node)

    def get_array(self, node):
        n = utils.generate_int(self._array_min_count, self._array_max_count)
        items = [self._get_node(node['items']) for _ in range(n)]
        return items

    def _get_object(self, node):
        object = {}
        properties = {}
        if 'properties' in node:
            properties = node['properties']

        min_len = None

        if "minProperties" in node:
            min_len = node['minProperties']

        for field in properties:
            object[field] = self._get_node(properties[field])

        if min_len is not None and min_len > len(object):
            for i in range(min_len - len(object)):
                object[utils.generate_string(4)] = self._get_string({})

        return object

    def _get_string(self, node):
        min_len = self._default_len_min_string
        max_len = self._default_len_max_string
        if "pattern" in node:
            return rstr.xeger(node['pattern'])
        if "minLength" in node:
            min_len = node['minLength']
            additional_range = 20
            max_len = min_len + additional_range

        if "maxLength" in node:
            max_len = node['maxLength']

        return utils.generate_string_between(min_len, max_len)

    def _get_number(self, node):
        min_val = self._default_min_number
        max_val = self._default_max_number

        if 'minimum' in node:
            min_val = node['minimum']
        if 'exclusiveMinimum' in node and node['exclusiveMinimum'] is True:
            min_val += self._exclisuve_delta

        if 'maximum' in node:
            max_val = node['maximum']
        if 'exclusiveMaximum' in node and node['exclusiveMaximum'] is True:
            max_val -= self._exclisuve_delta

        result = utils.generate_float(min_val, max_val)

        if 'multipleOf' in node:
            mult = node['multipleOf']
            result = utils.generate_int(min_val / mult, max_val / mult) * mult
        return result


def get_json(schema):
    generator = JsonGenerator(schema)
    return generator.getJson()
