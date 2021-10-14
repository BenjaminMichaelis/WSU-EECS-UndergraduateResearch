from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config
from app.Controller.forms import PostForm, RegistrationForm, SortForm

from app import db
from app.Model.models import Post, Tag, postTags, User
from app.Controller.forms import PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.Controller.auth_forms import LoginForm
bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET','POST'])
@bp_routes.route('/index', methods=['GET','POST'])
@login_required
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    sortform = SortForm()
    if request.method == 'POST':
        selectdata = int(sortform.select.data)
        booleandata = bool(sortform.usersposts.data)
        if sortform.validate_on_submit():
            if booleandata == False:
                if selectdata == 3:
                    posts = Post.query.order_by(Post.timestamp.desc())
                if selectdata == 2:
                    posts = Post.query.order_by(Post.title.desc())
                if selectdata == 1:
                    posts = Post.query.order_by(Post.likes.desc())
                if selectdata == 0:
                    posts = Post.query.order_by(Post.happiness_level.desc())
            elif booleandata == True:
                if selectdata == 3:
                    posts = current_user.get_user_posts().order_by(Post.timestamp.desc())
                if selectdata == 2:
                    posts = current_user.get_user_posts().order_by(Post.title.desc())
                if selectdata == 1:
                    posts = current_user.get_user_posts().order_by(Post.likes.desc())
                if selectdata == 0:
                    posts = current_user.get_user_posts().order_by(Post.happiness_level.desc())
            # print(selectdata, type(sortform.select.data).__name__)
            print(booleandata, type(sortform.usersposts.data).__name__)
    return render_template('index.html', title="Smile Portal", posts=posts.all(), sform = sortform)

@bp_routes.route('/delete/<postid>', methods=['POST'])
@login_required
def delete(postid):
    currentPost=Post.query.filter_by(id=postid).first()
    PostTitle = currentPost.title
    if currentPost is None:
        flash('Post with id "{}" not found.'.format(postid))
        return redirect(url_for('routes.index'))
    for t in currentPost.tags:
        currentPost.tags.remove(t)
    db.session.commit()
    db.session.delete(currentPost)
    flash('Post "{}" has been successfully deleted'.format(PostTitle))
    return redirect(url_for('routes.index'))

@bp_routes.route('/like/<postid>', methods=['POST'])
@login_required
def like(postid):
    # TODO: (milestone1)  add "like" button
    currentPost=Post.query.filter_by(id=postid).first()
    if currentPost is None:
        flash('Post with id "{}" not found.'.format(postid))
        return redirect(url_for('routes.index'))
    currentPost.likes += 1
    db.session.commit()
    flash('Post Liked.')
    posts = Post.query.order_by(Post.timestamp.desc())
    return redirect(url_for('routes.index'))

@bp_routes.route('/postsmile', methods=['POST','GET'])
@login_required
def postsmile():
    # handle the form submission
    sform = PostForm()
    if request.method == 'POST':
        if sform.validate_on_submit():
            newPost = Post(title = sform.title.data, body = sform.body.data, happiness_level = sform.happiness_level.data, user_id = current_user.id)
            for tag in sform.tag.data:
                newPost.tags.append(tag)
            print(newPost)
            db.session.add(newPost)
            db.session.commit()
            flash('New Post ' + newPost.title + " is posted")
            return redirect(url_for('routes.index'))
        pass
    return render_template('create.html', form = sform)