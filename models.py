from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from flask_login import LoginManager, UserMixin 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader 

def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    password= db.Column(db.String(128), nullable=False)
    date_created = (db.Column(db.DateTime, default=datetime.utcnow))
    tasks = db.relationship('Todo', backref='owned_user', lazy=True)
    
    def __repr__(self):
        return '<User %r>' % self.id

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default = False)
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
      
    def __repr__(self):
        return '<Task %r>' % self.id