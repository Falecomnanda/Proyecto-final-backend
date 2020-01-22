import os
from flask import Flask, render_template, jsonify, request, Blueprint
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_cors import CORS
from models import db, Category, User, Post
from routes.category import route_categories
from routes.user import route_user
from routes.auth import auth
from flask_jwt_extended import(JWTManager)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'dev.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret' #change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(delta=3)

jwt = JWTManager(app)
db.init_app(app)

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

@app.route('/')
def home():
    return render_template('index.html', name='home')

app.register_blueprint(auth)
app.register_blueprint(route_categories, url_prefix = '/api')
app.register_blueprint(route_user, url_prefix = '/api')
    


def Post(id= None):
    if request.method == 'GET':
        if id is not None:
            post = Post.query.get(id)
            if post:
                return jsonify(post.serialize()), 200
            else: 
                return jsonify({'post': 'not found'}), 400
        else:
            posts = Post.query.all()
            posts = list(map(lambda post: post.serialize(), posts))
            return jsonify(posts), 200   
    
    if request.method == 'POST':
        #validar la informacao

        post = Post()
        post.description = request.json.get('description')

        db.session.add(post)
        db.session.commit()

        return jsonify(posts), 201
    
    if request.method == 'PUT':

        post = Post.query.get(id)
        post.description = request.json.get('description')

        
        db.session.commit()

        return jsonify(post.serialize()), 200

   
    if request.method == 'DELETE':
        post = Post.query.get(id)
        db.session.delete(post)

        db.session.commit()

        return jsonify({'post': 'deleted'}), 400

if __name__ =='__main__':
    manager.run()    