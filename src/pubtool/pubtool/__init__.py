from flask import (Flask,
    render_template, current_app, Blueprint, redirect, _request_ctx_stack, request)

from pubtool.routes import create_routes
from pubtool.database import mongo

app = Flask(__name__)
app.config.from_object("pubtool.config.DevelopmentConfig")
app.config['PROPAGATE_EXCEPTIONS'] = True

mongo.init_app(app)

bp = Blueprint('pubtool', __name__,
                        template_folder='templates')
create_routes(bp)

@app.route('/')
def home():
    return redirect('/manage')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.errorhandler(401)
def permission_denied(e):
    return render_template('401.html'), 401

@app.before_request
def before_request():
    method = request.args.get('_method', '').upper()
    if method:
        request.environ['REQUEST_METHOD'] = method
        ctx = _request_ctx_stack.top
        ctx.url_adapter.default_method = method
        assert request.method == method

app.register_blueprint(bp, url_prefix='/manage')