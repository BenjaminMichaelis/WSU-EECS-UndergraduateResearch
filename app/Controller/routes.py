from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Controller.forms import PostForm
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