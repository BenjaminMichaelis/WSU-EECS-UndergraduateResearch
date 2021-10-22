from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import  ValidationError, DataRequired, EqualTo, Length,Email
from app.Model.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register')


    def validate_email(form, email):
        valid_domain = str('wsu.edu')
        domain = form.domainsplit(email.data).lower()
        if domain != valid_domain:
            raise ValidationError('Email must be valid wsu.edu email')
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email or username is already registered!')
    
    def domainsplit(self,email):
        try:
            return email.split('@')[1]
        except:
            return 'not a domain'

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This email or username is already registered!')