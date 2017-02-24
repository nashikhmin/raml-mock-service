# This module validate arguments of requests
from common import message


def validate(input, expected):
    validator = Validator(expected)
    validator.validate(input)


class Validator:
    def __init__(self, expected_values):
        self.arguments = expected_values

    def get_template_argument(self, arg):
        for t_arg in self.arguments:
            if t_arg.name == arg:
                return t_arg
        return None

    def validate(self, input):
        for arg in input:
            t_arg = self.get_template_argument(arg)
            if t_arg:
                self.validate_argument(input[arg], t_arg)
                # TODO add checking required params

    def validate_argument(self, value, params):
        if params.type == 'string':
            self.validate_string(value, params)
        elif params.type == 'number':
            self.resolve_number(value, params)

        elif params.type == 'integer':
            self.resolve_integer(value, params)
        elif params.type == 'date':
            self.resolve_date(value, params)
        elif params.type == 'bool':
            self.resolve_bool(value, params)
        elif params.type == 'file':
            self.resolve_file(value, params)
        else:
            pass

    def resolve_bool(raw_value, param):
        value = float(raw_value)

    def resolve_file(raw_value, param):
        pass

    def resolve_integer(raw_value, param):
        pass

    def resolve_date(raw_value, param):
        pass

    def resolve_number(raw_value, param):
        pass

    def validate_string(self, raw_value, param):
        value = str(raw_value)
        if param.min_length and param.min_length > len(value):
            raise Exception(message.ERR_STRING_MIN)
        if param.max_length and param.max_length < len(value):
            raise Exception(message.ERR_STRING_MAX)
        if param.enum and not raw_value in param.enum:
            raise Exception(message.ERR_STRING_ENUM)