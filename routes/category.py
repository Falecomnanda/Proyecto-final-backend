from flask import Blueprint, request, jsonify
from models import db, Category

route_categories = Blueprint('route_categories', __name__)

@route_categories.route('/categories', methods=['GET','POST'])
@route_categories.route('/categories/<int:id>', methods=['GET', 'PUT', 'DELETE']) 

def categories(id= None):
    if request.method == 'GET':
        if id is not None:
            category = Category.query.get(id)
            if category:
                return jsonify(category.serialize()), 200
            else: 
                return jsonify({'category': 'not found'}), 400
        else:
            categories = Category.query.all()
            categories = list(map(lambda category: category.serialize(), categories))
            return jsonify(categories), 200   
    
    if request.method == 'POST':
        #validar la informacao

        category = Category()
        category.description = request.json.get('description')

        db.session.add(category)
        db.session.commit()

        return jsonify(category.serialize()), 201
    
    if request.method == 'PUT':

        category = Category.query.get(id)
        category.description = request.json.get('description')

        
        db.session.commit()

        return jsonify(category.serialize()), 200

   
    if request.method == 'DELETE':
        category = Category.query.get(id)
        db.session.delete(category)

        db.session.commit()

        return jsonify({'category': 'deleted'}), 400

