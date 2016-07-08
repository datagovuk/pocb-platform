import json

from flask import Flask, current_app
from flask.ext.testing import TestCase
from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

from pubtool.database import mongo
from pubtool.routes import create_routes

class BaseTest(TestCase):

    def create_app(self):
        app = Flask('pubtool')
        app.secret_key = "testing"
        app.config.from_object("pubtool.config.TestingConfig")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['PROPAGATE_EXCEPTIONS'] = True
        mongo.init_app(app)

        #login_manager = LoginManager()
        #login_manager.init_app(app)

        #@login_manager.user_loader
        #def load_user(user_id):
        #   from olaf.models import User
        #    return db.session.query(User).filter(User.id==user_id).first()

        create_routes(app)

        self.test_app = app.test_client()
        self.test_app.testing = True

        return app

    def setUp(self):
        self.create_localtest_data(mongo)

    def tearDown(self):
        # Remove Test Index from Elastic
        mongo.db.publishers.remove({})

    def create_localtest_data(self, mongo):
        pass

    def do_get(self, url, json=False):
        return self.test_app.get(url)

    def do_post(self, url, data, json=False):
        headers = {}
        if json:
            headers = {'content-type':'application/json'}
        return self.test_app.get(url, headers=headers, data=data)

    def response_as_json(self, response):
        import json
        body = response.data.decode('utf-8')
        return json.loads(body)