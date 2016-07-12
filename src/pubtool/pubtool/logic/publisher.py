from .base import LogicObject

from pubtool.database import mongo
from pubtool.lib.schema import validation_check, ObjectValidationErrors

class Publisher(LogicObject):

    @classmethod
    def create(cls, data):
        errors = validation_check("publisher", data)
        if errors:
            raise ObjectValidationErrors(errors)

        mongo.db.publishers.insert_one(data)
        return cls.clean(data)

    @classmethod
    def get(cls, id):
        return cls.clean(mongo.db.publishers.find_one({'name': id}))

    def update(self, id):
        errors = validation_check("publisher", data)
        if errors:
            raise ObjectValidationErrors(errors)
        return {}

    @classmethod
    def delete(cls, id):
        # TODO: We should probably just return a bool or something here
        # because atomic ops or something.
        object = Publisher.get(id)
        if not object: return None

        mongo.db.publishers.delete_one({'name': id})
        return cls.clean(object)

    @classmethod
    def list(cls):
        return [cls.clean(p) for p in mongo.db.publishers.find()]
