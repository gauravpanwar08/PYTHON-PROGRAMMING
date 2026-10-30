from flask import Blueprint

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    return "Welcome to Flask Home Page"

@home_bp.route("/about")
def about():
    return "About Flask Application"

