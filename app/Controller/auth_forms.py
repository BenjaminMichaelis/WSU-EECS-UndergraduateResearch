from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField
from wtforms.validators import  NumberRange, ValidationError, DataRequired, EqualTo, Length,Email
from app.Model.models import User

import math

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone Number')
    wsuid = IntegerField('WSUID')
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_phone(form, phone):
        number = form.phone.data
        count = 0
        if type(number) is int:
            while (number > 0):
                number = number//10
                count = count + 1
            if count < 10 or count > 11:
                raise ValidationError('Not a valid phone number')
        else:
            raise ValidationError('Please make sure your phone number contains only integers')

    def validate_wsuid(form, wsuid):
        id = form.wsuid.data
        count = 0
        if type(id) is int:
            while (id > 0):
                id = id//10
                count = count + 1
            if count < 8 or count > 9:
                raise ValidationError('Not a valid WSU ID')
        else:
            raise ValidationError('Please make sure your WSU ID contains only integers')

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
        username.data = (username.data).strip()
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This email or username is already registered!')