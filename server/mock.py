import json

import ramlfications
from flask import Flask, request

from server.jsongenerator.jsongenerator import get_json
from server.validator import validate


class Mock:
    def __init__(self, raml_file):
        self.parser = ramlfications.parse(raml_file)
        self.app = Flask(__name__)

    def start(self, port, debug=False):
        self._init_url_rules()
        self.app.run(host='0.0.0.0', port=port, debug=debug)

    def _init_url_rules(self):
        for resource in self.parser.resources:
            self.app.add_url_rule(
                rule=self._transrofm_path_raml_to_flask(resource.path) + '/',  # I believe this is the actual url
                endpoint=resource.name,  # this is the name used for url_for (from the docs)
                view_func=self.get,
                defaults={'route': resource.path},
                methods=['GET']
            )

    def _transrofm_path_raml_to_flask(self, s):
        s = s.replace('{', '<')
        s = s.replace('}', '>')
        return s

    def _get_endpoint(self, route):
        return next((resource for resource in self.parser.resources if resource.path == route), None)

    def _get_response(self, resource, method):
        return next((responce for responce in resource.responses if responce.method == method), None)

    # handle GET requests
    def get(self, route, **kwargs):
        endpoint = self._get_endpoint(route)
        validate(request.args, endpoint.query_params)
        response = self._get_response(endpoint, 'get')
        json_body = next((body for body in response.body if body.mime_type == 'application/json'), None)

        if json_body.schema:
            result = get_json(json_body.schema)
        else:
            result = json_body.example

        return json.dumps(result)
