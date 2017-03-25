import json

import rstr as rstr

import server.jsongenerator.utils as utils


class JsonGenerator:
    _array_min_count = 4
    _array_max_count = 10

    _default_len_min_string = 3
    _default_len_max_string = 26


    def __init__(self, schema):
        self.data = json.loads(schema)

        self._types = {
            'object': self.get_object,
            'string': self.get_string,
            'array': self.get_array,
            'number': self.get_number,
        }

    def getJson(self):
        return self.get_node(self.data)

    def get_node(self, node):
        # TODO: improve and delete this statement
        if 'type' not in node:
            return None
        type = node['type']
        if isinstance(type, list):
            return self._types[type[0]](node)
        return self._types[type](node)

    def get_array(self, node):
        n = utils.generate_int(self._array_min_count, self._array_max_count)
        items = [self.get_node(node['items']) for _ in range(n)]
        return items

    def get_object(self, node):
        object = {}
        properties = {}
        if 'properties' in node:
            properties=node['properties']

        max_len = None

        if "maxProperties" in node:
            max_len = node['maxProperties']

        for field in properties:
            object[field] = self.get_node(properties[field])
        if max_len is not None and min_len>len(object):
            for i in range(min_len-len(object)):
                object[utils.generate_string(4)]=self.get_string({})

        return object

    def get_string(self, node):
        if "enum" in node:
            enum = node["enum"]
            i = utils.generate_int(0, len(enum) - 1)
            return enum[i]

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

    def get_number(self, node):
        return utils.generate_int()


def getJson(schema):
    generator = JsonGenerator(schema)
    return generator.getJson()
