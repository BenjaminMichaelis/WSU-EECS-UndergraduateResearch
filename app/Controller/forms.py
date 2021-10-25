from enum import unique
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField, IntegerField, FormField, DateField
from wtforms.fields.core import IntegerField
from wtforms.validators import  DataRequired, Length, ValidationError, EqualTo, Email, Optional
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget

from app.Model.models import Post, Field, User

def get_fields():
    return Field.query.all()

def get_fieldlabel(thefield):
    return thefield.name

class PostForm(FlaskForm):
    title = StringField('Position Title', validators=[DataRequired()])
    description = TextAreaField('Position Details', [Length(min=1, max=1500)])
    startdate = DateField('Start Date MM-DD-YYYY', format='%m-%d-%Y', validators=[DataRequired(message="Required, must be in MM-DD-YYYY")])
    enddate = DateField('End Date MM-DD-YYYY', format='%m-%d-%Y', validators=[DataRequired(message="Required, must be in MM-DD-YYYY")])
    timecommitment = IntegerField('Time Commitment (in Hours Per Week)', validators=[DataRequired()])
    ResearchFields = QuerySelectMultipleField('Research Fields', query_factory=get_fields , get_label=get_fieldlabel, widget=ListWidget(prefix_label=False), 
      option_widget=CheckboxInput() )
    qualifications = TextAreaField('Required Qualifications', [Length(min=1, max=1500)])
    submit = SubmitField('Post')

class EditForm(FlaskForm):
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    wsuid = IntegerField('WSUID', [Length(min=8, max=9)])
    major = StringField('Major')
    gpa = StringField('GPA', validators=[Length(max=4)])
    graduationDate = DateField('Expected Graduation')
    phone = FormField(TelephoneForm)
    password = PasswordField('Password', validators=[EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat Password')
    submit = SubmitField('Submit')

class TelephoneForm(FlaskForm):
    country_code = IntegerField('Country Code', validators=[DataRequired()])
    area_code    = IntegerField('Area Code/Exchange', validators=[DataRequired()])
    number       = StringField('Number')

# class SortForm(FlaskForm):
#     select = SelectField('Select',choices = [(3,'Date'),(2,'Title'),(1,'# of likes'),(0,'Happiness level')])
#     usersposts = BooleanField('Display my posts only.')
#     submit = SubmitField('Refresh')