from flask import jsonify
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

def list():
    publishers = Publisher.list()
    return _api_success(publishers, {'count': len(publishers)})

def show(slug):
    publisher = Publisher.get(slug)
    if not publisher:
        return _api_error(["Publisher could not be found"])
    return _api_success(publisher)