from flask import Flask
from flask import json
from flask_restful import Api
import ramlfications

RAML_FILE = "example.raml"
parser = ramlfications.parse(RAML_FILE)
a = parser.resources[0].responses[0].body[0].example

app = Flask(__name__)
api = Api(app)


def init_url_rules():
    for resource in parser.resources:
        app.add_url_rule(
            rule=transrofm_path_raml_to_flask(resource.path) + '/',  # I believe this is the actual url
            endpoint=resource.name,  # this is the name used for url_for (from the docs)
            view_func=get,
            defaults={'route': resource.path},
            methods=['GET']
        )


def transrofm_path_raml_to_flask(s):
    s =s.replace('{','<')
    s = s.replace('}', '>')
    return s

# it is the handler of get requests
# TODO: params
def get(route, **kwargs):
    resourse = next((resourse for resourse in parser.resources if resourse.path == route), None)
    responce = next((responce for responce in resourse.responses if responce.method == 'get'), None)
    json_answer = next((body.example for body in responce.body if body.mime_type == 'application/json'), None)
    return json.dumps(json_answer)


if __name__ == '__main__':
    init_url_rules()
    app.run(debug=True)
