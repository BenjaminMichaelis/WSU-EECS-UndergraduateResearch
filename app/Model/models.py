from datetime import datetime
from enum import unique
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

userFields = db.Table('userFields',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('field_id', db.Integer, db.ForeignKey('field.id'))
)

postFields = db.Table('postFields',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('field_id', db.Integer, db.ForeignKey('field.id'))
)

applications = db.Table('applications',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('application_id', db.Integer, db.ForeignKey('application.id'))
)

userLanguages = db.Table('userLanguages',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('language_id', db.Integer, db.ForeignKey('language.id'))
)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    description = db.Column(db.String(1500))
    startdate = db.Column(db.Date)
    enddate = db.Column(db.Date)
    timecommitment = db.Column(db.Integer)
    qualifications = db.Column(db.String(1500))
    sharedFieldCount = db.Column(db.Integer)
    ResearchFields = db.relationship(
        'Field',  secondary = postFields,
        primaryjoin=(postFields.c.post_id == id), backref=db.backref('postFields', lazy='dynamic')
        , lazy='dynamic')
    Applications = db.relationship(
        'Application',  secondary = applications,
        primaryjoin=(applications.c.post_id == id), backref=db.backref('applications', lazy='dynamic')
        , lazy='dynamic')
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    db.relationship('User', backref="Userid", lazy='dynamic')

    def get_Applications(self):
        return self.Applications

    def get_ResearchFields(self):
        return self.ResearchFields

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer)
    preferredname = db.Column(db.String(100))
    description = db.Column(db.String(1500))
    referenceName = db.Column(db.String(50))
    referenceEmail = db.Column(db.String(50))
    approved = db.Column(db.Boolean, default=False)
    hired = db.Column(db.Boolean, default=False)
    nothired = db.Column(db.Boolean, default=False)

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
    wsuid = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    major = db.Column(db.String(30))
    gpa = db.Column(db.Float)
    graduationDate = db.Column(db.Date)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    experience = db.Column(db.Text)
    electiveCourses = db.Column(db.Text)
    approved = db.Column(db.Boolean, default=False)
    hired = db.Column(db.Boolean, default=False)

    Fields = db.relationship(
        'Field',  secondary = userFields,
        primaryjoin=(userFields.c.user_id == id), backref=db.backref('userFields', lazy='dynamic')
        , lazy='dynamic')

    LanguagesKnown = db.relationship(
        'Language',  secondary = userLanguages,
        primaryjoin=(userLanguages.c.user_id == id), backref=db.backref('userLanguages', lazy='dynamic'),
        lazy='dynamic')

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

    def get_Languages(self):
        return self.LanguagesKnown

    def get_fields(self):
        return self.Fields

    def get_LanguagesCount(self):
        count = 0
        for language in self.get_Languages():
            count += 1
        return count

    def get_FieldsCount(self):
        count = 0
        for field in self.get_fields():
            count += 1
        return count

    def remove_languages(self):
        for language in self.LanguagesKnown:
            self.LanguagesKnown.remove(language)
        db.session.commit()

    def remove_fields(self):
        for field in self.Fields:
            self.Fields.remove(field)
        db.session.commit()

class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

    def __repr__(self):
        return '<Language name: {} Language id: {}'.format(self.name,self.id)

@login.user_loader
def load_user(username):
    return User.query.get(username)