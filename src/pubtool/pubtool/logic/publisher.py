from .base import LogicObject

from pubtool.database import mongo

class Publisher(LogicObject):

    def create(self, data):
        pass

    @classmethod
    def get(cls, id):
        return cls.clean(mongo.db.publishers.find_one({'slug': id}))

    def update(self, id):
        pass

    def delete(self, id):
        pass

    @classmethod
    def list(cls):
        return [cls.clean(p) for p in mongo.db.publishers.find()]
