from flask import Blueprint

api = Blueprint('tings_api', __name__)

@api.route('/')
def welcome():
    return "welcome to our api fam"
