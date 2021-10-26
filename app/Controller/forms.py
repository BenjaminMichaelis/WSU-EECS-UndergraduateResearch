from enum import unique
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField, DateField
from wtforms.fields.core import IntegerField
from wtforms.validators import  DataRequired, Length, ValidationError, EqualTo, Email, Optional
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget

from app.Model.models import Post, Tag, User

def get_tags():
    return Tag.query.all()

def get_taglabel(thetag):
    return thetag.name

class PostForm(FlaskForm):
    title = StringField('Position Title', validators=[DataRequired()])
    description = TextAreaField('Position Details', [Length(min=1, max=1500)])
    startdate = DateField('Start Date MM-DD-YYYY', format='%m-%d-%Y', validators=[DataRequired(message="Required, must be in MM-DD-YYYY")])
    enddate = DateField('End Date MM-DD-YYYY', format='%m-%d-%Y', validators=[DataRequired(message="Required, must be in MM-DD-YYYY")])
    timecommitment = IntegerField('Time Commitment (in Hours Per Week)', validators=[DataRequired()])
    ResearchFields = QuerySelectMultipleField( 'Major', query_factory=get_tags , get_label=get_taglabel, widget=ListWidget(prefix_label=False), 
      option_widget=CheckboxInput() )
    qualifications = TextAreaField('Required Qualifications', [Length(min=1, max=1500)])
    submit = SubmitField('Post')

# class SortForm(FlaskForm):
#     select = SelectField('Select',choices = [(3,'Date'),(2,'Title'),(1,'# of likes'),(0,'Happiness level')])
#     usersposts = BooleanField('Display my posts only.')
#     submit = SubmitField('Refresh')