import re

from flask import jsonify, request
from pubtool.database import mongo
from pubtool.logic import Publisher

def _api_success(response, extra=None):
    '''
    A successful call will return the data wrapped in a
    success/data object.  It is possible to pass extra
    top level keys which will be added to the response.
    '''
    data = {
        'data': response,
        'success': True
    }
    if extra:
        data.update(extra)
    return jsonify(data)

def _api_error(errors, status_code=404):
    '''
    When an API call fails, this will wrap the response and make
    sure that the errors are returned to the user. By default we
    will assume a 404, but it is possible for the actual status
    code to be passed in to this function.
    '''
    return jsonify({
        'errors': errors,
        'success': False
    }), status_code

def api_home():
    return jsonify({'version': 1})


# This tuple contains a list of tuples representing the possible API calls
# that can be made by a user.  The API is found by a match on the first
# element of the tuple, and the function to call is the second element.
API = (
    (re.compile("publisher/(.*)"),  Publisher.get, ["GET"]),
    (re.compile("publisher/(.*)"),  Publisher.delete, ["DELETE"]),
    (re.compile("publisher$"),      Publisher.list, ["GET"]),
)

def api_call(path):
    '''
    This is the primary function through which all API calls are made.
    The request path is used to determine which logic class/function to
    call with the appropriate arguments from the path.  Query parameters
    should still be available on the request object for the logic layer to use
    if necessary '''
    result = None

    # Iterate through all the known URLs until we find a path that matches.
    # We're not expecting many
    for k, f, allowed_verbs in API:
        m = k.match(path)
        if not m:
            continue

        if not request.method in allowed_verbs:
            continue

        # If it is a path with an argument, then call the function passing in the
        # arguments
        if m.groups():
            args = [a for a in m.groups()]
            result = f(*args)
        else:
            result = f()

        if not result and not result == []:
            return _api_error(["Unable to locate the requested item"])
        else:
            return _api_success(result)

    return _api_error(["Unknown API call"])

