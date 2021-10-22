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

    valid_domain = str('wsu.edu')

    def validate_email(form, email):
        domain = form.domainsplit(email.data).lower()
        print(domain, type(domain).__name__)
        if domain != form.valid_domain:
            print(form.valid_domain, type(form.valid_domain).__name__)
            print(domain, type(domain).__name__)
            raise ValidationError('Email must be valid wsu.edu email')
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email or username is already registered!')
    
    def domainsplit(self,emailaddress):
        try:
            return emailaddress.split('@')[1]
        except:
            return 'not a domain'

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This email or username is already registered!')