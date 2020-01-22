from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from models import db, User
from flask_jwt_extended import (
    jwt_required
)

bcrypt = Bcrypt()
route_user = Blueprint('route_user', __name__)

@route_user.route('/users', methods=['GET','POST'])
@route_user.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required 
def users(id= None):
    if request.method == 'GET':
        if id is not None:
            user = User.query.get(id)
            if user:
                return jsonify(user.serialize()), 200
            else: 
                return jsonify({'user': 'not found'}), 400
        else:
            users = User.query.all()
            users = list(map(lambda user: user.serialize(), users))
            return jsonify(users), 200   
    
    if request.method == 'POST':
        #validar la informacao
        password = request.json.get('password')
        user = User()
        user.username = request.json.get('username')
        user.email = request.json.get('email')
        user.password = bcrypt.generate_password_hash(password)

        db.session.add(user)
        db.session.commit()

        return jsonify(user.serialize()), 201
    
    if request.method == 'PUT':
        password = request.json.get('password')
        user = User.query.get(id)
        user.username = request.json.get('username')
        user.email = request.json.get('email')
        user.password = bcrypt.generate_password_hash(password)
        
        db.session.commit()

        return jsonify(user.serialize()), 200

   
    if request.method == 'DELETE':
        user = Post.query.get(id)
        db.session.delete(user)

        db.session.commit()

        return jsonify({'user': 'deleted'}), 400