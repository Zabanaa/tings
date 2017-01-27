from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('tings.config.BaseConfig')
db  = SQLAlchemy(app)

@app.route('/')
def index():
    return "Hello Mad World"

if __name__ == "__main__":
    app.run(host="0.0.0.0")
