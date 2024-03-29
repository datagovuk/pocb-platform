'''
A collection of validation functions.  These are registered in pubtool.lib.validators with a
name that appears in the JSON Schema.

The functions here whould contain:
    validator - The validator that is being used
    value - The value of the validation function, i.e. the name it was registered with
    instance - The value of the property
    schema - The schema subset for the current property
'''
import re

from pubtool.database import mongo

from jsonschema.exceptions import ValidationError

def load_validators():
    return {
        'unique_publisher': unique_publisher_validator,
        'slug': slug_validator,
    }

def unique_publisher_validator(validator, value, instance, schema):
    """ Checks the object name being validated does not already exist """
    existing = mongo.db.publishers.find_one({'name': instance})
    if existing:
        return [ValidationError("'name' is already in use", instance=instance, validator=validator)]
    return None

def slug_validator(validator, value, instance, schema):
    """ Make sure the field looks like a slug """
    # instance
    if not re.match(r'^[-a-zA-Z0-9_]+\Z', instance):
        return [ValidationError(
            "'name' should consist only of lowercase letters, numbers, underscores or hyphens",
            instance=instance,
            validator=validator)]
