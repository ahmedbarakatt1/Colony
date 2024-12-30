from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from database_setup import get_db
from models import User

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/register', methods=['POST'])
def register():
    db = next(get_db())
    data = request.form
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], Email=data['email'], password=hashed_password)
    db.add(new_user)
    db.commit()
    return jsonify({"message": "User registered successfully!"}), 201


