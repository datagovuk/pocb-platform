from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object("frontend.config.DevelopmentConfig")
app.config['PROPAGATE_EXCEPTIONS'] = True

#create_routes(app)
#create_filters(app)

@app.route('/')
def hello_world():
    return 'Hello, World from frontend!'