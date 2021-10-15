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
from app.Model.models import User, Post, Tag
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


def init_tags():
    # initialize the tags
    if Tag.query.count() == 0:
        tags = ['funny','inspiring', 'true-story', 'heartwarming', 'friendship']
        for t in tags:
            db.session.add(Tag(name=t))
        db.session.commit()
        print(tags)
    return None

@pytest.fixture
def init_database():
    # Create the database and the database table
    db.create_all()
    # initialize the tags
    init_tags()
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
    assert response.status_code == 200
    assert b"Register" in response.data

def test_register(test_client,init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register' form is submitted (POST)
    THEN check that the response is valid and the database is updated correctly
    """
    # Create a test client using the Flask application configured for testing
    response = test_client.post('/register', 
                          data=dict(username='john', email='john@wsu.edu',password="bad-bad-password",password2="bad-bad-password"),
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
    response = test_client.post('/login', 
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
    response = test_client.post('/login', 
                          data=dict(username='sakire', password='1234',remember_me=False),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Smile Portal!" in response.data

    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data

def test_postSmile(test_client,init_database):
    """
    GIVEN a Flask application configured for testing , after user logs in,
    WHEN the '/postsmile' page is requested (GET)  AND /PostForm' form is submitted (POST)
    THEN check that response is valid and the class is successfully created in the database
    """
    #login
    response = test_client.post('/login', 
                        data=dict(username='sakire', password='1234',remember_me=False),
                        follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Smile Portal!" in response.data
    
    #test the "PostSmile" form 
    response = test_client.get('/postsmile')
    assert response.status_code == 200
    assert b"Post New Smile" in response.data
    
    #test posting a smile story
    tags1 = list( map(lambda t: t.id, Tag.query.all()[:3]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
    print("TESTING********************: ", tags1)
    response = test_client.post('/postsmile', 
                          data=dict(title='My test post', body='This is my first test post.',happiness_level=2, tag = tags1),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Smile Portal!" in response.data
    assert b"My test post" in response.data 
    assert b"This is my first test post." in response.data 

    c = db.session.query(Post).filter(Post.title =='My test post')
    assert c.first().get_tags().count() == 3 #should have 3 tags
    assert c.count() >= 1 #There should be at least one post with body "Here is another post."


    tags2 = list( map(lambda t: t.id, Tag.query.all()[1:3]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
    print("TESTING********************: ", tags2)
    response = test_client.post('/postsmile', 
                          data=dict(title='Second post', body='Here is another post.',happiness_level=1, tag = tags2),
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Smile Portal!" in response.data
    assert b"Second post" in response.data 
    assert b"Here is another post." in response.data 

    c = db.session.query(Post).filter(Post.body =='Here is another post.')
    assert c.first().get_tags().count() == 2  # Should have 2 tags
    assert c.count() >= 1 #There should be at least one post with body "Here is another post."

    assert db.session.query(Post).count() == 2

    #finally logout
    response = test_client.get('/logout',                       
                          follow_redirects = True)
    assert response.status_code == 200
    assert b"Sign In" in response.data

def test_likeSmile(test_client,init_database):
    """
    GIVEN a Flask application configured for testing , after user logs-in,
     /like form is submitted (POST)
    THEN check that response is valid and the like count is updated in the database
    """
    #login
    response = test_client.post('/login', 
                        data=dict(username='sakire', password='1234',remember_me=False),
                        follow_redirects = True)
    assert response.status_code == 200
    assert b"Welcome to Smile Portal!" in response.data
    
    #first post two smile stories
    response = test_client.get('/postsmile')
    assert response.status_code == 200
    tags1 = list( map(lambda t: t.id, Tag.query.all()[:3]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
    response = test_client.post('/postsmile', 
                          data=dict(title='My test post', body='This is my first test post.',happiness_level=2, tag = tags1),
                          follow_redirects = True)
    assert response.status_code == 200
    c1 = db.session.query(Post).filter(Post.title =='My test post')
    assert c1.count() >= 1 #There should be at least one post with body "Here is another post."


    tags2 = list( map(lambda t: t.id, Tag.query.all()[1:3]))  # should only pass 'id's of the tags. See https://stackoverflow.com/questions/62157168/how-to-send-queryselectfield-form-data-to-a-flask-view-in-a-unittest
    response = test_client.post('/postsmile', 
                          data=dict(title='Second post', body='Here is another post.',happiness_level=1, tag = tags2),
                          follow_redirects = True)
    assert response.status_code == 200
    c2 = db.session.query(Post).filter(Post.body =='Here is another post.')
    assert c2.count() >= 1 #There should be at least one post with body "Here is another post."
    assert c2.first().likes == 0 
    assert db.session.query(Post).count() == 2

    #like the second post 
    response = test_client.post('/like/'+str(c2.first().id), 
                          data={},
                          follow_redirects = True)
    assert response.status_code == 200
    #The page should be redirected to the main page
    assert b"Welcome to Smile Portal!" in response.data
    #check whether the likecount was updated successfully
    c3 = db.session.query(Post).filter(Post.id ==c1.first().id)
    assert c3.first().likes == 0 
    c4 = db.session.query(Post).filter(Post.id ==c2.first().id)
    assert c4.first().likes == 1     

    

# def test_enroll(request,test_client,init_database):
#     """
#     GIVEN a Flask application configured for testing , after user logs in, and after a class is created
#     WHEN the '/enroll' form is submitted (POST)
#     THEN check that response is valid and the currently logged in user (student) is successfully added to roster
#     """
#     #first login
#     response = test_client.post('/login', 
#                           data=dict(username='sakire', password='1234',remember_me=False),
#                           follow_redirects = True)
#     assert response.status_code == 200
#     assert b"Hi, Sakire Arslan Ay!" in response.data
    
#     #create a class
#     response = test_client.post('/createclass', 
#                           data=dict(coursenum = '355', title = 'Programming Languages', major = 'CptS'),
#                           follow_redirects = True)
#     assert response.status_code == 200
#     c = db.session.query(Class).filter(Class.coursenum =='355')
#     assert c.count() == 1

#     #enroll the logged in student in CptS 355
#     response = test_client.post('/enroll/'+str(c.first().id), 
#                         data=dict(),
#                         follow_redirects = True)
#     assert response.status_code == 200
#     assert b"You are now enrolled in class CptS 355!" in response.data
#     c = db.session.query(Class).filter(Class.coursenum =='355' and Class.major == 'CptS')
#     assert c.first().roster[0].username == 'sakire'

#     #finally logout
#     response = test_client.get('/logout',                       
#                           follow_redirects = True)
#     assert response.status_code == 200
#     assert b"Sign In" in response.data
#     assert b"Please log in to access this page." in response.data   


# def test_login(request,test_client,init_database):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/' page is requested (GET)
#     THEN check that the response is valid
#     """
#     response = test_client.post('/login', 
#                           data=dict(username='sakire', password='1234',remember_me=False),
#                           follow_redirects = True)
#     assert response.status_code == 200
#     assert b"Hi, Sakire Arslan Ay!" in response.data
