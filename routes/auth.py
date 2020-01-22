from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, get_jwt_identity
)
from flask_bcrypt import Bcrypt
from models import db, User

bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "username is required"}), 422
    if not password:
        return jsonify({"msg": "password is required"}), 422
    
    user = User.query.filter_by(username = username).first()

    if not user:
        return jsonify({"msg": "username not found"}), 422

    
    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        data = {
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 200
    else:
        return jsonify({"msg": "username/password are incorrect"}), 401



@auth.route('/register', methods = ['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    if not username:
        return jsonify({"msg": "username is required"}), 422
    if not password:
        return jsonify({"msg": "password is required"}), 422
    if not email:
        return jsonify({"msg": "email is required"}), 422

    user = User.query.filter_by(username = username).first()

    if user:
        return jsonify({"msg": "username is taken"}), 200

    user = User()
    user.username =  username
    user.email = email
    user.password = bcrypt.generate_password_hash(password) 

    db.session.add(user)
    db.session.commit()    

    
    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username)
        data = {
            "access_token": access_token,
            "user": user.serialize()
        }
        return jsonify(data), 200
    else:
        return jsonify({"msg": "username/password are incorrect"}), 401