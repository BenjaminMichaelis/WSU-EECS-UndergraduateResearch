from __future__ import print_function
import os
import sys
from flask import Blueprint, send_from_directory
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Controller.forms import PostForm, EditForm, EditPasswordForm, ApplyForm, AddFieldForm, RemoveFieldForm, SortForm
from flask_login import current_user, login_user, logout_user, login_required
from app.Controller.auth_forms import LoginForm, RegistrationForm
from app.Model.models import Post, Application, User, Field
bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'

@bp_routes.route('/', methods=['GET','POST'])
@bp_routes.route('/index/', methods=['GET','POST'])
@login_required
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    postscount = Post.query.count()
    print(postscount)
    sform = SortForm()
    if sform.validate_on_submit():
        order = sform.select.data
        if order == '0':

            for post in posts.all():
                cnt = 0
                for pfield in post.ResearchFields:
                    for ufield in current_user.Fields:
                        if ufield.id == pfield.id:
                            cnt+=1
                            break
                post.sharedFieldCount = cnt
                print(cnt)
                db.session.add(post)
                db.session.commit()
            posts = Post.query.order_by(Post.sharedFieldCount.desc())
        elif order == '1':
            posts = Post.query.order_by(Post.title.asc())
        elif order == '2':
            posts = Post.query.order_by(Post.timecommitment.desc())

    return render_template('index.html', title="WSU Undergraduate Research Portal", posts=posts.all(), User = User, postscount = postscount, sortForm = sform)

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
            current_user.phone = eform.phone.data
            current_user.major = eform.major.data
            current_user.gpa = eform.gpa.data
            current_user.graduationDate = eform.graduationDate.data
            current_user.experience = eform.experience.data
            current_user.electiveCourses = eform.electives.data
            for language in eform.languages.data:
                current_user.LanguagesKnown.append(language)
            for field in eform.fields.data:
                current_user.Fields.append(field)
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
        eform.electives.data = current_user.electiveCourses
    else:
        pass
    return render_template('edit_profile.html', title='Edit Profile', form = eform)

@bp_routes.route('/edit_password/', methods=['GET', 'POST'])
@login_required
def edit_password():
    pform = EditPasswordForm()
    if request.method == 'POST':
        if pform.validate_on_submit():
            current_user.set_password(pform.password.data)
            db.session.add(current_user)
            db.session.commit()
            flash("Your password has been changed")
            return redirect(url_for('routes.display_profile'))
        pass
    return render_template('edit_password.html', title='Edit Password', form = pform)

@bp_routes.route('/apply/<post_id>', methods=['POST'])
@login_required
def apply(post_id):
    aform = ApplyForm()
    post = Post.query.filter_by(id=post_id).first()
    if request.method == 'POST':
        if aform.validate_on_submit():
            newApp = Application(userid=current_user.id, preferredname = aform.preferredname.data, description=aform.description.data, referenceName=aform.refName.data, referenceEmail=aform.refEmail.data)
            post.Applications.append(newApp)
            db.session.add(newApp)
            db.session.commit()
            flash("You have successfully applied to this position")
            return redirect(url_for('routes.index'))
        pass
    return render_template('apply.html', title='Apply', form = aform)

@bp_routes.route('/delete/<post_id>', methods=['POST'])
@login_required
def delete(post_id):
    # only faculty can create delete their research positions
    if current_user.faculty is True:
        currentPost=Post.query.filter_by(id=post_id).first()
        if currentPost is None:
            flash('Post with id "{}" not found.'.format(post_id))
            return redirect(url_for('routes.index'))
        PostTitle = currentPost.title
        for t in currentPost.ResearchFields:
            currentPost.ResearchFields.remove(t)
        for t in currentPost.Applications:
            currentPost.Applications.remove(t)
        db.session.delete(currentPost)
        db.session.commit()
        flash('Post "{}" has been successfully deleted'.format(PostTitle))
        return redirect(url_for('routes.index'))
    flash('Error: No faculty permissions discovered')
    return redirect(url_for('routes.index'))

@bp_routes.route('/myposts/', methods=['POST','GET'])
@login_required
def myposts():
    if current_user.faculty is True:
    # only faculty can view their own posts
        posts = Post.query.filter_by(user_id=current_user.id)
        return render_template('index.html', title="My Research Postings", posts=posts.all(), User = User)
    flash('Error: No faculty permissions discovered')
    return redirect(url_for('routes.index'))

@bp_routes.route('/add_field/', methods=['GET', 'POST'])
@login_required
def add_field():
    if current_user.admin is True:
        aform = AddFieldForm()
        if request.method == 'POST':
            # handle the form submission
            if aform.validate_on_submit():
                newField = Field(name=aform.newfieldname.data)
                db.session.add(newField)
                db.session.commit()
                flash("Field has been added")
                return redirect(url_for('routes.index')) #html for admin page
        return render_template('add_fields.html', title='Edit Fields', form = aform) #html for admin page
    flash('Error: No admin permissions discovered')
    return redirect(url_for('routes.index'))

@bp_routes.route('/remove_field/', methods=['GET', 'POST'])
@login_required
def remove_field():
    if current_user.admin is True:
        rform = RemoveFieldForm()
        if request.method == 'POST':
            # handle the form submission
            if rform.validate_on_submit():
                for field in rform.ResearchFields.data:
                    # remove field from database
                    # User.query.filter_by(id=123).delete()
                    # Field.query.filter_by(name=field.name).delete()
                    db.session.delete(field)
                # db.session.add(newField)
                db.session.commit()
                flash("Field(s) have been removed")
                return redirect(url_for('routes.index')) #html for admin page
        return render_template('remove_fields.html', title='Edit Fields', form = rform) #html for admin page
    flash('Error: No admin permissions discovered')
    return redirect(url_for('routes.index'))

@bp_routes.route('/cancelApplication/<application_id>/', methods=['POST','DELETE'])
@login_required
def cancelApplication(application_id):
    if current_user.faculty is False:
        application = Application.query.filter_by(id=application_id).first()
        if application.approved == True:
            flash('You had been approved for an interview. Please inform the professor that you have canceled your application!')
        db.session.delete(application)
        db.session.commit()
        flash('Application has been canceled')
    return redirect(url_for('routes.index'))

@bp_routes.route('/favicon.ico')
def favicon():
    path_list=[bp_routes.root_path,os.pardir,"View","static","img"]
    print(bp_routes.root_path)
    print(os.path.join(*path_list))
    return send_from_directory(os.path.join(*path_list),
        'favicon.ico',mimetype='image/vnd.microsoft.icon')