from .base import LogicObject

from pubtool.database import mongo
from pubtool.lib.schema import validation_check, ObjectValidationErrors
from pubtool.search import index_item, delete_item

from flask import request

class Publisher(LogicObject):

    @classmethod
    def create(cls, data):
        errors = validation_check("publisher", data)
        if errors:
            raise ObjectValidationErrors(errors)

        mongo.db.publishers.insert_one(data)
        obj = cls.clean(data)
        index_item('publisher', obj)
        return obj

    @classmethod
    def search(cls):
        print(request.args)
        return []

    @classmethod
    def get(cls, id):
        # TODO(RJ): Attach dependent objects
        return cls.clean(mongo.db.publishers.find_one({'name': id}))

    def update(self, id):
        errors = validation_check("publisher", data)
        if errors:
            raise ObjectValidationErrors(errors)
        index_item('publisher', data)
        return {}

    @classmethod
    def delete(cls, id):
        if not cls.get(id):
            return False

        mongo.db.publishers.delete_one({'name': id})
        delete_item('publisher', id)
        return True

    @classmethod
    def list(cls):
        return [cls.clean(p) for p in mongo.db.publishers.find()]
