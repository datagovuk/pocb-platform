import json
import logging

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, MatchAll

log = logging.getLogger(__name__)

def init_search(app, clean=False):
    """ Create a client and attach it to the app """
    elastic_hosts = json.loads(app.config.get('ELASTIC_HOSTS'))
    app.elastic_client = Elasticsearch(elastic_hosts)
    app.elastic_index_name = app.config.get('ELASTIC_INDEX')

    index_client = IndicesClient(app.elastic_client)
    log.info("Checking for index {} at {}".format(app.elastic_index_name, elastic_hosts))

    if index_client.exists(app.elastic_index_name):
        if clean:
            index_client.delete(app.elastic_index_name)
            index_client.create(app.elastic_index_name)
    else:
        index_client.create(app.elastic_index_name)

def search_for(item_type, q, extras=None):
    from flask import current_app

    es = current_app.elastic_client
    ix = current_app.elastic_index_name

    s = Search(using=es, index=ix, doc_type=item_type)
    s = s.query(MultiMatch(query=q, fields=['title']))
    return s.execute()


def index_item(item_type, data):
    from flask import current_app

    es = current_app.elastic_client
    ix = current_app.elastic_index_name

    if not es.exists( index=ix, doc_type=item_type, id=data['name']):
        log.info("Indexing: {}".format(data['name']))
        es.index(
            index=ix,
            doc_type=item_type,
            id=data['name'],
            body=data
         )
    else:
        log.info("Updating index: {}".format(data['name']))
        es.update(
            index=ix,
            doc_type=item_type,
            id=data['name'],
            body={'doc': data}
         )

    es.indices.refresh(index=ix)

def delete_item(item_type, id):
    from flask import current_app

    es = current_app.elastic_client
    ix = current_app.elastic_index_name
    if es.exists( index=ix, doc_type=item_type, id=id):
        log.info("Deleting from index: {}".format(id))
        es.delete(index=ix,
                             doc_type=item_type,
                             id=id)

def clear_index(app):
    """ Remove everything from the search index """
    index_client = IndicesClient(app.elastic_client)
    log.info("Clearing index {}".format(app.elastic_index_name))
    if index_client.exists(app.elastic_index_name):
        index_client.delete(app.elastic_index_name)
