from enum import unique
from flask_wtf import FlaskForm
from wtforms import DecimalField, StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField, IntegerField, FormField, DateField
from wtforms.fields.core import IntegerField
from wtforms.validators import  DataRequired, Length, ValidationError, EqualTo, Email, Optional
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget

import math

from app.Model.models import Language, Post, User, Field

def get_fields():
    return Field.query.all()

def get_fieldlabel(thefield):
    return thefield.name

def get_languages():
    return Language.query.all()

def get_languageLabel(thelanguage):
    return thelanguage.name

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
    apply = SubmitField('Apply')

class ApplyForm(FlaskForm):
    preferredname = StringField('Your preferred name: ', validators=[DataRequired()])
    description = TextAreaField('Describe why you are interested and what you hope to gain from this project', [Length(min=1, max=1500)])
    refName = StringField('Name of faculty member reference', validators=[DataRequired()])
    refEmail = StringField('Reference Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Apply')

class EditForm(FlaskForm):
    firstname = StringField('First Name')
    lastname = StringField('Last Name')
    major = StringField('Major')
    gpa = DecimalField('GPA', validators=[Optional()])
    graduationDate = DateField('Expected Graduation MM-DD-YYYY', format='%m-%d-%Y', validators=[Optional()])
    phone = IntegerField('Phone Number')
    experience = TextAreaField('Describe any prior experience you may have')
    electives = TextAreaField('Enter the technical elective courses you completed and the grade you received')
    languages = QuerySelectMultipleField('Languages you have experience in', query_factory=get_languages, get_label=get_languageLabel, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    fields = QuerySelectMultipleField('Research topics you are interested in', query_factory=get_fields, get_label=get_fieldlabel, widget=ListWidget(prefix_label=False), option_widget=CheckboxInput())
    submit = SubmitField('Save')

    def validate_phone(form, phone):
        number = form.phone.data
        count = 0
        while (number > 0):
            number = number//10
            count = count + 1
        if count < 10 or count > 11:
            raise ValidationError('Not a valid phone number')

    def validate_wsuid(form, wsuid):
        id = form.wsuid.data
        count = 0
        while (id > 0):
            id = id//10
            count = count + 1
        if count < 8 or count > 9:
            raise ValidationError('Not a valid WSU ID')

class SortForm(FlaskForm):
    select = SelectField('sortOrder', choices=[(0,'Recommended'),(1,'Title'),(2,'Time Commitment')])
    #recommended = BooleanField('Show Recommended Positions Only')
    submit = SubmitField('Refresh')

class EditPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat Password')
    submit = SubmitField('Save')

class AddFieldForm(FlaskForm):
    newfieldname = StringField('New Field:')
    submit = SubmitField('Save')

class RemoveFieldForm(FlaskForm):
    ResearchFields = QuerySelectMultipleField('Fields to remove', query_factory=get_fields , get_label=get_fieldlabel, widget=ListWidget(prefix_label=False),
    option_widget=CheckboxInput() )
    submit = SubmitField('Save')
