"""
This file contains the functional tests for the routes.
These tests use GETs and POSTs to different URLs to check for the proper behavior.
Resources:
    https://flask.palletsprojects.com/en/1.1.x/testing/ 
    https://www.patricksoftwareblog.com/testing-a-flask-application-using-pytest/ 
"""
import os
import pytest
from app import create_app, db
from app.Model.models import User, Post, Field
from config import Config


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True



@pytest.fixture(scope='module')
def test_client():
    # create the flask application ; configure the app for tests
    flask_app = create_app(config_class=TestConfig)

    db.init_app(flask_app)
    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield  testing_client 
    # this is where the testing happens!
 
    ctx.pop()

def new_user(uname, uemail,passwd):
    user = User(username=uname, email=uemail)
    user.set_password(passwd)
    return user


def init_fields():
    # initialize the fields
    if Field.query.count() == 0:
        fields = ['TestField1', 'TestField2','TestField3','TestField4','TestField5']
        for t in fields:
            db.session.add(Field(name=t))
        db.session.commit()
        print(fields)
    return None

@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_all()
    # initialize the tags
    init_fields()
    #add a user    
    user1 = new_user(uname='sakire', uemail='sakire@wsu.edu',passwd='1234')
    # Insert user data
    db.session.add(user1)
    # Commit the changes for the users
    db.session.commit()

    yield  # this is where the testing happens!

    db.drop_all()

def test_register_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' page is requested (GET)
    THEN check that the response is valid
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.get('/register')
    assert response.status_code == 308
    # assert b"Register" in response.data

def test_register(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/register/', 
                          data=dict(username='john', firstname='john', lastname='doe', email='john@wsu.edu', phone=1234567890, wsuid = 123456789, password="bad-bad-password",password2="bad-bad-password"),
                          follow_redirects = True)
    assert response.status_code == 200

    s = db.session.query(User).filter(User.username=='john')
    assert s.first().email == 'john@wsu.edu'
    assert s.count() == 1
    assert b"Sign In" in response.data   
    assert b"Please log in to access this page." in response.data

def test_invalidlogin(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with wrong credentials
    THEN check that the response is valid and login is refused 
    """
    response = test_client.post('/login/', 
                          data=dict(username='sakire', password='12345',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Invalid username or password" in response.data

def test_login_logout(request,test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' form is submitted (POST) with correct credentials
    THEN check that the response is valid and login is succesfull 
    """
    response = test_client.post('/login/', 
                          data=dict(username='sakire', password='1234',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"WSU Undergraduate Research Portal" in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data

def test_postResearch(test_client,init_database):
    """
    GIVEN a Flask application configured for testing , after user logs in,
    WHEN the '/postsmile' page is requested (GET)  AND /PostForm' form is submitted (POST)
    THEN check that response is valid and the class is successfully created in the database
    """
    #login
    response = test_client.post('/login/', 
                        data=dict(username='sakire', password='1234',remember_me=False),
                        follow_redirects = True)
    assert response.status_code == 200
    assert b"WSU Undergraduate Research Portal" in response.data
    
    
    #test the "PostSmile" form 
    response = test_client.get('/post/')
    assert response.status_code == 302
    



    
