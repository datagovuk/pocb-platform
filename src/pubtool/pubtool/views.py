from flask import render_template
from pubtool.database import mongo
from pubtool.logic import Publisher

def home():
    #mongo.db.publishers.insert_one({'name': 'Test publisher', 'slug': 'testpub'})
    #mongo.db.users.find_one_or_404({'_id': 'ross'})
    return render_template("index.html")

def publisher_list():
    ctx = {'publishers': Publisher.list()}
    return render_template("publisher/index.html", **ctx)

def publisher_show(slug):
    ctx = {'publisher': Publisher.get(slug)}
    return render_template("publisher/show.html", **ctx)