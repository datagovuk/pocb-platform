import os
import json

from pubtool.search import index_item
from pubtool import logic

from flask import current_app
from flask.ext.script import Command
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MatchAll

class InfoCommand(Command):
    ''' Import preset JSON files to the search engine '''

    name = "info"

    def run(self):
        print("Database contains\n=================")
        db_publisher_list = logic.Publisher.list()
        print("{} Publisher(s)".format(len(db_publisher_list)))

        print("\nSearch engine contains\n=================")

        es = current_app.elastic_client
        ix = current_app.elastic_index_name

        res = es.search(
            index = ix,
            doc_type="publisher", size=0)
        print("{} Publisher(s)".format(res['hits']['total']))