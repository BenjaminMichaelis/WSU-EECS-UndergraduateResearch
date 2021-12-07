from flask import Flask, send_from_directory
import os
from config import Config
from flask_sqlalchemy import SQLAlchemy
# TODO: (milestone 3) import LoginManager and Moment extensions here
from flask_login import LoginManager
from flask_moment import Moment

db = SQLAlchemy()
# TODO: (milestone 3) create LoginManager object and configure the login view as 'auth.login', i.e, `login` route in `auth` Blueprint. 
login = LoginManager()
login.login_view = 'auth.login'
# TODO: (milestone 3) create Moment object
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.static_folder = config_class.STATIC_FOLDER 
    app.template_folder = config_class.TEMPLATE_FOLDER

    db.init_app(app)
    # TODO: (milestone 3) Configure the app object for login using `init_app` function. 
    login.init_app(app)
    # TODO: (milestone 3) Configure the app object for moment using `init_app` function. 
    moment.init_app(app)

    @app.route('/favicon.ico')
    def favicon():
        path_list=[app.root_path,"View","static","img"]
        print(app.root_path)
        print(os.path.join(*path_list))
        return send_from_directory(os.path.join(*path_list),
            'favicon.ico',mimetype='image/vnd.microsoft.icon')

    # blueprint registration
    from app.Controller.errors import bp_errors as errors
    app.register_blueprint(errors)
    from app.Controller.auth_routes import bp_auth as auth
    app.register_blueprint(auth)
    from app.Controller.routes import bp_routes as routes
    app.register_blueprint(routes)

    if not app.debug and not app.testing:
        pass
        # ... no changes to logging setup
    

    return app
