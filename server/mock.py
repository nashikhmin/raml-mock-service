import ramlfications
from flask import Flask, request

from server.validator import validate


class Mock:
    def __init__(self, raml_file):
        self.parser = ramlfications.parse(raml_file)
        self.app = Flask(__name__)

    def start(self, debug=True):
        self._init_url_rules()
        # self.app.run(debug=debug)
        self.app.run(host='0.0.0.0', debug=debug)

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

    def _get_resource(self, route):
        return next((resource for resource in self.parser.resources if resource.path == route), None)

    def _get_response(self, resource, method):
        return next((responce for responce in resource.responses if responce.method == method), None)

    # it is the handler of get requests
    def get(self, route, **kwargs):
        resource = self._get_resource(route)
        validate(request.args, resource.query_params)
        response = self._get_response(resource, 'get')
        body = next((body for body in response.body if body.mime_type == 'application/json'), None)
        if (body.schema):
            json = body.schema
        else:
            json = body.example
        return json.dumps(json)
