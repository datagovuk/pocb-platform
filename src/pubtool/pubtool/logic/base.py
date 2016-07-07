


class LogicObject(object):

    def create(self, data):
        pass

    def get(self, id):
        pass

    def update(self, id):
        pass

    def delete(self, id):
        pass

    @classmethod
    def list(cls):
        pass

    @classmethod
    def clean(cls, object):
        if not object:
            return None
        return {k:v for k,v in object.items() if k[0] != '_'}