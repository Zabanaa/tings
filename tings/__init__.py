from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

# Init App
app = Flask(__name__)

# Import Config
app.config.from_envvar('TINGS_CONFIG')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB Init
db  = SQLAlchemy(app)

from tings.api.views import api
from tings.auth.views import auth

# Register Blueprints
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(auth, url_prefix="/auth")

@app.errorhandler(404)
def page_not_found(error):
    return "{} not found".format(request.url), 404

@app.route('/')
def index():
    return "Welcome to our api"
