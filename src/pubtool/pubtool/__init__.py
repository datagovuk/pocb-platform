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