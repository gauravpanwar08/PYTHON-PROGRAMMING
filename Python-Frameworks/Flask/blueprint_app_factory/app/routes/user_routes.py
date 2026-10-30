from flask import Blueprint, jsonify

user_bp = Blueprint("users", __name__)


@user_bp.route("/users")
def get_users():
    users = [
        {"id": 1, "name": "Gaurav"},
        {"id": 2, "name": "Rahul"}
    ]
    return jsonify(users)


@user_bp.route("/users/<int:user_id>")
def get_user(user_id):
    return jsonify({
        "id": user_id,
        "message": "User details fetched"
    })
    