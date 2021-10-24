from datetime import datetime
from enum import unique
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

postFields = db.Table('postFields',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('field_id', db.Integer, db.ForeignKey('field.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(1500))
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    timecommitment = db.Column(db.Integer)
    qualifications = db.Column(db.String(1500))
    Fields = db.relationship(
        'Field',  secondary = postFields,
        primaryjoin=(postFields.c.post_id == id), backref=db.backref('postFields', lazy='dynamic')
        , lazy='dynamic')
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    db.relationship('User', backref="Userid", lazy='dynamic')

    def get_fields(self):
        return self.Fields

class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    
    def __repr__(self):
        return '<Field name: {} Field id: {}'.format(self.name,self.id)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='writer', lazy='dynamic')
    faculty = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<id: {} - username {}>'.format(self.id, self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def get_password(self,password):
        return check_password_hash(self.password_hash, password)

    def get_user_posts(self):
        return self.posts

@login.user_loader
def load_user(username):
    return User.query.get(username)