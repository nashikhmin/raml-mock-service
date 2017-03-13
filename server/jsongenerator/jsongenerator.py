import json

import server.jsongenerator.utils as utils


class JsonGenerator:
    _array_min_count = 4
    _array_max_count = 10

    def __init__(self, file):
        json_data = open(file).read()
        self.data = json.loads(json_data)

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
        if not 'type' in node:
            return None
        type = node['type']
        return self._types[type](node)

    def get_array(self, node):
        n = utils.generate_number(self._array_min_count, self._array_max_count)
        items = [self.get_node(node['items']) for _ in range(n)]
        return items

    def get_object(self, node):
        object = {}
        properties = node['properties']
        for field in properties:
            object[field] = self.get_node(properties[field])
        return object

    def get_string(self, node):
        return utils.generate_string(10)

    def get_number(self, node):
        return utils.generate_number()


def getJson(schema):
    pass
generator = JsonGenerator('example.json')
a = generator.getJson()
print(a)
