from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(200))
    identity = db.relationship('Identity', backref='user', uselist=False)

class Identity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.String(10))
    email = db.Column(db.String(150))
    college = db.Column(db.String(150))
    student_id = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
