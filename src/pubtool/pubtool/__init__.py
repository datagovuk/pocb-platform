from flask import Flask, render_template, current_app, Blueprint, redirect

app = Flask(__name__)
app.config.from_object("pubtool.config.DevelopmentConfig")
app.config['PROPAGATE_EXCEPTIONS'] = True

#create_routes(app)
#create_filters(app)
bp = Blueprint('pubtool', __name__,
                        template_folder='templates')

@app.route('/')
def home():
    return redirect('/manage')

@bp.route('/')
def home():
    return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.errorhandler(401)
def permission_denied(e):
    return render_template('401.html'), 401

app.register_blueprint(bp, url_prefix='/manage')