from .base import LogicObject

from pubtool.database import mongo
from pubtool.lib.schema import validation_check

class Publisher(LogicObject):

    def create(self, data):
        errors = validation_check("publisher", data)

    @classmethod
    def get(cls, id):
        return cls.clean(mongo.db.publishers.find_one({'slug': id}))

    def update(self, id):
        errors = validation_check("publisher", data)

    @classmethod
    def delete(cls, id):
        # TODO: We should probably just return a bool or something here
        # because atomic ops or something.
        object = Publisher.get(id)
        if not object: return None

        mongo.db.publishers.delete_one({'slug': id})
        return cls.clean(object)

    @classmethod
    def list(cls):
        return [cls.clean(p) for p in mongo.db.publishers.find()]
