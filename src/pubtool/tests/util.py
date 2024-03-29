import json

from flask import Flask, current_app, request, _request_ctx_stack
from flask.ext.testing import TestCase
from flask.ext.login import LoginManager

from pubtool.search import init_search, clear_index
from pubtool.database import mongo
from pubtool.routes import create_routes

def before_request():
    method = request.args.get('_method', '').upper()
    if method:
        request.environ['REQUEST_METHOD'] = method
        ctx = _request_ctx_stack.top
        ctx.url_adapter.default_method = method
        assert request.method == method

class BaseTest(TestCase):

    def create_app(self):
        app = Flask('pubtool')
        app.secret_key = "testing"
        app.config.from_object("pubtool.config.TestingConfig")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['PROPAGATE_EXCEPTIONS'] = True
        mongo.init_app(app)

        init_search(app, clean=True)
        app.before_request(before_request)

        login_manager = LoginManager()
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            return {}

        create_routes(app)


        self.test_app = app.test_client()
        self.test_app.testing = True
        self.app = app
        return app

    def setUp(self):
        mongo.db.publishers.remove({})
        self.create_localtest_data(mongo)

    def tearDown(self):
        # Remove Test Index from Elastic and database
        clear_index(self.app)
        mongo.db.publishers.remove({})

    def create_localtest_data(self, mongo):
        pass

    def do_get(self, url, json=False):
        return self.test_app.get(url)

    def do_post(self, url, data, is_json=False):
        headers = {}
        if is_json:
            headers = {'content-type':'application/json'}
        return self.test_app.post(url, headers=headers, data=json.dumps(data), follow_redirects=True)

    def response_as_json(self, response):
        import json
        body = response.data.decode('utf-8')
        return json.loads(body)
