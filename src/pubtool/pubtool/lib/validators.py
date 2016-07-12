from pubtool.database import mongo

from jsonschema.exceptions import ValidationError

def unique_publisher_validator(validator, value, instance, schema):
    """ Checks the object name being validated does not already exist """
    existing = mongo.db.publishers.find_one({'name': instance})
    if existing:
        return [ValidationError("'name' is already in use", instance=instance, validator=validator)]
    return None
