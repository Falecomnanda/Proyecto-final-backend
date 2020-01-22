from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    #mi tabla de categoria creada
    description = db.Column(db.String(50), nullable=False)


    def __repr__(self):
        return '<Category %r>' % self.id

    def serialize(self):
        return{
            'id': self.id,
            'description': self.description
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    #mi tabla de categoria creada
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
        
        }   

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)    
    title = db.Column(db.String(255), nullable=False)     
    resume = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship(User)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(User)


    def __repr__(self):
        return '<Post %r>' % self.title

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title, 
            'resume': self.resume, 
            'content': self.content,
            'category': self.category.serialize(), 
            'user': self.user.serialize()
 
        }  

class PostMedia(db.Model):

    __tablename__ = 'PostMedia'
    id = db.Column(db.Integer, primary_key=True)
    #mi tabla de categoria creada
    username = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)     
    resume = db.Column(db.String(255), nullable=False)
    content = db.Column(db.String(255), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship(User)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship(User)
    

    def __repr__(self):
        return '<PostMedia %r>' % self.username

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'category': self.category.serialize(), 
        }   