import json
import logging

from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

log = logging.getLogger(__name__)

def init_search(app):
    """ Create a client and attach it to the app """
    elastic_hosts = json.loads(app.config.get('ELASTIC_HOSTS'))
    app.elastic_client = Elasticsearch(elastic_hosts)
    app.elastic_index_name = app.config.get('ELASTIC_INDEX')

    index_client = IndicesClient(app.elastic_client)
    log.info("Checking for index {} at {}".format(app.elastic_index_name, elastic_hosts))
    if index_client.exists(app.elastic_index_name):
        index_client.delete(app.elastic_index_name)
        index_client.create(app.elastic_index_name)

def clear_index(app):
    """ Remove everything from the search index """
    index_client = IndicesClient(app.elastic_client)
    log.info("Clearing index {}".format(app.elastic_index_name))
    if index_client.exists(app.elastic_index_name):
        index_client.delete(app.elastic_index_name)
