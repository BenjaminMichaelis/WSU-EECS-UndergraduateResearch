from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Controller.forms import PostForm, EditForm
from flask_login import current_user, login_user, logout_user, login_required
from app.Controller.auth_forms import LoginForm, RegistrationForm
from app.Model.models import Post
bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET','POST'])
@bp_routes.route('/index/', methods=['GET','POST'])
@login_required
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('index.html', title="WSU Undergraduate Research Portal", posts=posts.all())

@bp_routes.route('/post/', methods=['POST','GET'])
@login_required
def post():
    # only faculty can create new research positions
    if current_user.faculty is True:
        # handle the form submission
        sform = PostForm()
        if request.method == 'POST':
            if sform.validate_on_submit():
                newPost = Post(title = sform.title.data, description = sform.description.data, user_id = current_user.id, 
                startdate = sform.startdate.data, enddate = sform.enddate.data, timecommitment = sform.timecommitment.data,
                qualifications = sform.qualifications.data)
                for ResearchFields in sform.ResearchFields.data:
                    newPost.ResearchFields.append(ResearchFields)
                print(newPost)
                db.session.add(newPost)
                db.session.commit()
                flash('New Post ' + newPost.title + " is posted")
                return redirect(url_for('routes.index'))
            pass
        return render_template('create.html', form = sform)
    flash('Error: No faculty permissions discovered')
    return redirect(url_for('routes.index'))

@bp_routes.route('/display_profile/', methods=['GET'])
@login_required
def display_profile():
    return render_template('display_profile.html', title='Display Profile', user = current_user)

@bp_routes.route('/edit_profile/', methods=['GET', 'POST'])
@login_required
def edit_profile():
    eform = EditForm()
    if request.method == 'POST':
        # handle the form submission
        if eform.validate_on_submit():
            current_user.firstname = eform.firstname.data
            current_user.lastname = eform.lastname.data
            current_user.set_password(eform.password.data)
            current_user.phone = eform.phone.data 
            current_user.major = eform.major.data 
            current_user.gpa = eform.gpa.data 
            current_user.graduationDate = eform.graduationDate.data 
            current_user.experience = eform.experience.data
            db.session.add(current_user)
            db.session.commit()
            flash("Your changes have been saved")
            return redirect(url_for('routes.display_profile'))
        pass
    elif request.method == 'GET':
        # populate the user data from DB
        eform.firstname.data = current_user.firstname
        eform.lastname.data = current_user.lastname
        eform.phone.data = current_user.phone 
        eform.major.data = current_user.major 
        eform.gpa.data = current_user.gpa 
        eform.graduationDate.data = current_user.graduationDate
        eform.experience.data = current_user.experience
    else:
        pass 
    return render_template('edit_profile.html', title='Edit Profile', form = eform)
