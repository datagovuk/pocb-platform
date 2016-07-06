from flask import Flask, render_template, current_app

app = Flask(__name__)
app.config.from_object("pubtool.config.DevelopmentConfig")
app.config['PROPAGATE_EXCEPTIONS'] = True

#create_routes(app)
#create_filters(app)

@app.route('/')
def home():
    print( current_app.config["ELASTIC_HOSTS"])
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
