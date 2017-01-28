from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tings.api.views import api
from tings.auth.views import auth

# Init App
app = Flask(__name__)

# Import Config
app.config.from_object('tings.config.BaseConfig')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# DB Init
db  = SQLAlchemy(app)

# Register Blueprints
app.register_blueprint(api, url_prefix="/api")
app.register_blueprint(auth, url_prefix="/auth")

@app.route('/')
def index():
    return "Hello Mad World"
