"""
Schema management for various object types (publisher, dataset etc).  Loads
the jsonschema and allows callers to validate a dictionary against them.
"""
import os
import json

import pubtool.lib.validators as v

from jsonschema import validate, validators
from jsonschema.exceptions import ValidationError

SCHEMA = {
    "publisher": None,
    "dataset": None
}

class ObjectValidationErrors(Exception):
    def __init__(self, errors):
        self.errors = errors

def _get_directory():
    p = os.path.dirname(__file__)
    p = os.path.join(p, os.pardir, os.pardir, "schema")
    p = os.path.abspath(p)
    return p

def _get_schema(name):
    """ Load, if necessary, the schema for the specific name
        and return it """
    global SCHEMA

    loaded_schema = SCHEMA.get(name)
    if not loaded_schema:
        filename = "{}/{}.json".format(_get_directory(), name)
        if os.path.exists(filename):
            SCHEMA[name] = json.load(open(filename, 'r'))

    return SCHEMA.get(name)

def validation_check(object_type, data):
    from jsonschema import Draft4Validator

    schema = _get_schema(object_type)
    if not schema:
        # raise ValidationError, not Exception
        raise Exception()

    new_validators = v.load_validators()

    custom_validator = validators.extend(
        Draft4Validator,
        validators=new_validators
    )
    validator = custom_validator(schema)

    errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
    errors = [v.message for v in errors]

    return errors