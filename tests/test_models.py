import warnings
warnings.filterwarnings("ignore")
import os
basedir = os.path.abspath(os.path.dirname(__file__))

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.Model.models import User, Post
from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ROOT_PATH = '..//'+basedir
    
class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='john', email='john.doe@wsu.edu')
        u.set_password('password')
        self.assertFalse(u.get_password('covid'))
        self.assertTrue(u.get_password('password'))

    def test_post_1(self):
        u1 = User(username='john', email='john.yates@wsu.com')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().all(), [])
        p1 = Post(title = 'My post', description = 'Some dope research', user_id = u1.id)
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().count(), 1)
        self.assertEqual(u1.get_user_posts().first().title, 'My post')
        self.assertEqual(u1.get_user_posts().first().description, 'Some dope research')
    
    def test_post_2(self):
        # create the users and add to the database
        u1 = User(username='John', email='john.doe@wsu.com')
        u2 = User(username='Jane', email='jane.doe@wsu.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        # tests that the users do not have any posts
        self.assertEqual(u1.get_user_posts().all(), [])
        self.assertEqual(u2.get_user_posts().all(), [])
        # create the posts
        p1 = Post(title='My post 1', description='This is my first test post.', user_id=u1.id)
        db.session.add(p1)
        p2 = Post(title='My post 2', description='This is my second test post.', user_id=u1.id)
        db.session.add(p2)
        p3 = Post(title='My post 3', description='This is a post by someone else.', user_id=u2.id)
        db.session.add(p3)
        db.session.commit()
        # test the posts by the first user
        self.assertEqual(u1.get_user_posts().count(), 2)
        self.assertEqual(u1.get_user_posts().all()[0].title, 'My post 1')
        self.assertEqual(u1.get_user_posts().all()[0].description, 'This is my first test post.')  
        self.assertEqual(u1.get_user_posts().all()[1].title, 'My post 2')
        self.assertEqual(u1.get_user_posts().all()[1].description, 'This is my second test post.')  
        # test the posts by the second user
        self.assertEqual(u2.get_user_posts().count(), 1)
        self.assertEqual(u2.get_user_posts().all()[0].title, 'My post 3')
        self.assertEqual(u2.get_user_posts().all()[0].description, 'This is a post by someone else.')

    def test_application_1(self):
        u1 = User(username='john', email='john.doe@wsu.com')
        db.session.add(u1)
        db.session.commit()
         

if __name__ == '__main__':
    unittest.main()
#     # def test_post_1(self):
#     #     u1 = User(username='john', email='john.yates@wsu.com')
#     #     db.session.add(u1)
#     #     db.session.commit()
#     #     self.assertEqual(u1.get_user_posts().all(), [])
#     #     p1 = Post(title='My post', body='This is my test post.', happiness_level=1, user_id=u1.id)
#     #     db.session.add(p1)
#     #     db.session.commit()
#     #     self.assertEqual(u1.get_user_posts().count(), 1)
#     #     self.assertEqual(u1.get_user_posts().first().title, 'My post')
#     #     self.assertEqual(u1.get_user_posts().first().body, 'This is my test post.')
#     #     self.assertEqual(u1.get_user_posts().first().happiness_level, 1)

#     # def test_post_2(self):
#     #     u1 = User(username='john', email='john.yates@wsu.com')
#     #     u2 = User(username='amit', email='amit.khan@wsu.com')
#     #     db.session.add(u1)
#     #     db.session.add(u2)
#     #     db.session.commit()
#     #     self.assertEqual(u1.get_user_posts().all(), [])
#     #     self.assertEqual(u2.get_user_posts().all(), [])
#     #     p1 = Post(title='My post 1', body='This is my first test post.', happiness_level=1, user_id=u1.id)
#     #     db.session.add(p1)
#     #     p2 = Post(title='My post 2', body='This is my second test post.', happiness_level=3, user_id=u1.id)
#     #     db.session.add(p2)
#     #     db.session.commit()
#     #     p3 = Post(title='Another post', body='This is a post by somebody else.', happiness_level=2, user_id=u2.id)
#     #     db.session.add(p3)
#     #     db.session.commit()
#     #     # test the posts by the first user
#     #     self.assertEqual(u1.get_user_posts().count(), 2)
#     #     self.assertEqual(u1.get_user_posts().all()[1].title, 'My post 2')
#     #     self.assertEqual(u1.get_user_posts().all()[1].body, 'This is my second test post.')
#     #     self.assertEqual(u1.get_user_posts().all()[1].happiness_level, 3)
#     #     # test the posts by the second user
#     #     self.assertEqual(u2.get_user_posts().count(), 1)
#     #     self.assertEqual(u2.get_user_posts().all()[0].title, 'Another post')
#     #     self.assertEqual(u2.get_user_posts().all()[0].body, 'This is a post by somebody else.')
#     #     self.assertEqual(u2.get_user_posts().all()[0].happiness_level, 2)
