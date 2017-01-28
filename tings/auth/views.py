from flask import Blueprint

auth = Blueprint("auth", __name__)

@auth.route('/register')
def register_user():
    return "register man"

@auth.route('/login')
def login_user():
    return "allow man in"

@auth.route('/logout')
def logout_user():
    return "see you cuz"

@auth.route('/me')
def check_user():
    return "who dat ?"
