'''
A base class to be implemented by objects providing logic functions.  This
class mostly just acts as documentation for new implementations and a
couple of helper functions.
'''


class LogicObject(object):

    def create(self, data):
        ''' Create a new object using the data passed in.  This data should be
            authorised and validated before insertion. '''
        pass

    def get(self, id):
        ''' Returns the data object with the given id '''
        pass

    def search(cls):
        ''' Uses the flask object to find out what the parameters are '''
        pass

    def update(self, id, data):
        ''' Update the object identified by id with the data provided '''
        pass

    def delete(self, id):
        ''' Delete the object identified by id '''
        pass

    @classmethod
    def list(cls):
        ''' Return a list of all the objects of this type '''
        pass

    @classmethod
    def clean(cls, object):
        ''' Iterates through the object and removes any key/value where the
        key starts with _, such as _id. We are following the python convention
        that _keys are private and should not be rendered for the user. '''
        if not object:
            return None
        return {k:v for k,v in object.items() if k[0] != '_'}