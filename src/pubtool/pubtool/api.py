import re

from flask import jsonify, request
from pubtool.database import mongo
from pubtool.logic import Publisher

def _api_success(response, extra=None):
    data = {
        'data': response,
        'success': True
    }
    if extra:
        data.update(extra)
    return jsonify(data)

def _api_error(errors):
    return jsonify({
        'errors': errors,
        'success': False
    })

def api_home():
    return jsonify({'version': 1})

API = (
    (re.compile("publisher/(.*)"), Publisher.get),
    (re.compile("publisher"), Publisher.list),
)

def api_call(path):
    result = None
    # Iterate through all the known URLs until we find a path that matches
    for k, f in API:
        m = k.match(path)
        if not m:
            continue

        # If it is a path with an argument, then call the function passing in the
        # arguments
        if m.groups():
            args = [a for a in m.groups()]
            result = f(*args)
        else:
            result = f()

        if result:
            return _api_success(result)
        else:
            return _api_error(["Unable to locate the requested item"])

    return _api_error(["Unknown API call"])

