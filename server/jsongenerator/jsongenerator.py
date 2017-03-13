import json
import random


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
        type = node['type']
        self._types[type](node)

    def get_array(self, node):
        n = random.randint(self._array_min_count, self._array_max_count)
        items = [] * n
        for item in items:
            item = self.get_node(node['items'])
        return items

    def get_object(self, node):
        pass

    def get_string(self, node):
        pass

    def get_number(self, node):
        pass


generator = JsonGenerator('example.json')
generator.getJson()
