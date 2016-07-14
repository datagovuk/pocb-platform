import os
import json

from pubtool.search import index_item
from pubtool import logic
from flask.ext.script import Command, Option

class SearchImportCommand(Command):
    ''' Import preset JSON files to the search engine '''

    name = "search_import"

    option_list = (
        Option("--inputfile", "-i", dest="inputfile"),
        Option("--type", "-t", dest="type"),
    )

    def run(self, inputfile, type):
        if not inputfile or not os.path.exists(inputfile):
            print("Missing input file. Please specify with -i </path/to/jsonfile>")
            return

        count = 0
        items = json.load(open(inputfile, 'r'))
        for item in items:
            index_item(type, item)
            count = count + 1

        print("Indexed {} items".format(count))


class DatabaseImportCommand(Command):
    ''' Import preset JSON files to Mongo, and also adds them to the search engine '''

    name = "database_import"

    option_list = (
        Option("--inputfile", "-i", dest="inputfile"),
        Option("--type", "-t", dest="type"),
    )

    def run(self, inputfile, type):
        if not inputfile or not os.path.exists(inputfile):
            print("Missing input file. Please specify with -i </path/to/jsonfile>")
            return

        types = {
            'publisher': logic.Publisher
        }

        update_count, insert_count = 0, 0

        obj = types[type]
        items = json.load(open(inputfile, 'r'))
        for item in items:
            id = item['name']
            if obj.get(id):
                obj.update(id, item)
                update_count += 1
            else:
                obj.create(item)
                insert_count = insert_count + 1

        print("Stored {} items and updated {} items".format(insert_count, update_count))
