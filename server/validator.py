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

        self.validate_required_components(input)

    def validate_required_components(self, input):
        for t_arg in self.arguments:
            if t_arg.required and t_arg.name not in input:
                raise Exception(message.ERR_REQUIRED_ARGUMENT)

    def validate_argument(self, value, params):
        if params.type == 'string':
            self.validate_string(value, params)
        elif params.type == 'number':
            self.validate_number(value, params)
        elif params.type == 'integer':
            self.validate_integer(value, params)
        elif params.type == 'date':
            self.resolve_date(value, params)
        elif params.type == 'bool':
            self.resolve_bool(value, params)
        elif params.type == 'file':
            self.resolve_file(value, params)
        else:
            pass

    def resolve_bool(raw_value, param):
        # TODO
        pass

    def resolve_file(raw_value, param):
        # TODO
        pass

    def resolve_integer(raw_value, param):
        # TODO
        pass

    def resolve_date(raw_value, param):
        # TODO
        pass

    def validate_integer(self, value, param):
        try:
            value = int(value)
        except:
            raise Exception(message.ERR_INTEGER)
        self._validate_min_max(value, param)

    def validate_number(self, value, param):
        try:
            value = float(value)
        except:
            raise Exception(message.ERR_NUMBER)
        self._validate_min_max(value, param)

    def _validate_min_max(self, value, param):
        if param.minimum is not None and param.minimum > value:
            raise Exception(message.ERR_MINIMUM)
        if param.maximum is not None and param.maximum < value:
            raise Exception(message.ERR_MAXIMUM)

    def validate_string(self, value, param):
        value = str(value)
        if param.min_length is not None and param.min_length > len(value):
            raise Exception(message.ERR_STRING_MIN)
        if param.max_length is not None and param.max_length < len(value):
            raise Exception(message.ERR_STRING_MAX)
        if param.enum is not None and value not in param.enum:
            raise Exception(message.ERR_STRING_ENUM)
            # TODO: validate pattern