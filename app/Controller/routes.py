from __future__ import print_function
import sys
from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request
from config import Config

from app import db
from app.Controller.forms import PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.Controller.auth_forms import LoginForm, RegistrationForm
bp_routes = Blueprint('routes', __name__)
bp_routes.template_folder = Config.TEMPLATE_FOLDER #'..\\View\\templates'


@bp_routes.route('/', methods=['GET','POST'])
@bp_routes.route('/index/', methods=['GET','POST'])
@login_required
def index():
            # print(selectdata, type(sortform.select.data).__name__)
            # print(booleandata, type(sortform.usersposts.data).__name__)
    return render_template('index.html', title="Smile Portal")