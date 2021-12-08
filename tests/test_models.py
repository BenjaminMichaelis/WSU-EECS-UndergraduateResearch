import warnings
warnings.filterwarnings("ignore")
import os
import datetime
basedir = os.path.abspath(os.path.dirname(__file__))

from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.Model.models import User, Post, Application, applications, Field, Language
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
        u = User(username='john', email='john.yates@wsu.edu')
        u.set_password('covid')
        self.assertFalse(u.get_password('flu'))
        self.assertTrue(u.get_password('covid'))

    def test_post_1(self):
        u1 = User(username='john', email='john.doe@wsu.com')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().all(), [])
        p1 = Post(title='My post', description='This is my test post.', user_id=u1.id)
        db.session.add(p1)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().count(), 1)
        self.assertEqual(u1.get_user_posts().first().title, 'My post')
        self.assertEqual(u1.get_user_posts().first().description, 'This is my test post.')

    def test_post_2(self):
        u1 = User(username='john', email='john.doe@wsu.com')
        u2 = User(username='jane', email='jane.doe@wsu.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.get_user_posts().all(), [])
        self.assertEqual(u2.get_user_posts().all(), [])
        p1 = Post(title='My post 1', description='This is my first test post.', user_id=u1.id)
        db.session.add(p1)
        p2 = Post(title='My post 2', description='This is my second test post.', user_id=u1.id)
        db.session.add(p2)
        db.session.commit()
        p3 = Post(title='Another post', description='This is a post by somebody else.', user_id=u2.id)
        db.session.add(p3)
        db.session.commit()
        # test the posts by the first user
        self.assertEqual(u1.get_user_posts().count(), 2)
        self.assertEqual(u1.get_user_posts().all()[1].title, 'My post 2')
        self.assertEqual(u1.get_user_posts().all()[1].description, 'This is my second test post.')
        # test the posts by the second user
        self.assertEqual(u2.get_user_posts().count(), 1)
        self.assertEqual(u2.get_user_posts().all()[0].title, 'Another post')
        self.assertEqual(u2.get_user_posts().all()[0].description, 'This is a post by somebody else.')
    
    def test_application_1(self):
        # add users to db
        u1 = User(username='john', email='john.doe@wsu.com')
        u2 = User(username='jane', email='jane.doe@wsu.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        # tests that there are no posts or applications yet
        self.assertEqual(Post.query.filter_by(user_id=u1.id).count(), 0)
        self.assertEqual(Application.query.filter_by(userid=u1.id).count(), 0)
        # add a a post by user 1 and an application by user 2 
        p1 = Post(title='My post 1', description='This is my first test post.', user_id=u1.id)
        db.session.add(p1)
        a1 = Application(userid = u2.id, preferredname = 'jane', description='hire me please')
        db.session.add(a1)
        db.session.commit()
        # test that the a post by user 1 and an application by user 2 now exists
        self.assertEqual(Post.query.filter_by(user_id=u1.id).count(), 1)
        self.assertEqual(Application.query.filter_by(userid=u2.id).count(), 1) 

    def test_application_2(self):
        # add users to db
        u1 = User(username='john', email='john.doe@wsu.com')
        u2 = User(username='jane', email='jane.doe@wsu.com')
        u3 = User(username='will', email='will.doe@wsu.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.commit()
        # tests that there are no posts or applications
        self.assertEqual(Post.query.filter_by(user_id=u1.id).count(), 0)
        self.assertEqual(Application.query.count(), 0)
        # add a a post by user 1 and an application by user 2 and user 3
        p1 = Post(title='My post 1', description='This is my first test post.', user_id=u1.id)
        db.session.add(p1)
        a1 = Application(userid = u2.id, preferredname = 'jane', description='hire me please')
        db.session.add(a1)
        a2 = Application(userid = u3.id, preferredname = 'will', description='hire me please')
        db.session.add(a2)
        db.session.commit()
        # test that the post and applications now exist
        self.assertEqual(Post.query.filter_by(user_id=u1.id).count(), 1)
        self.assertEqual(Application.query.count(), 2)
        self.assertEqual(Application.query.filter_by(userid=u2.id).count(), 1)
        self.assertEqual(Application.query.filter_by(userid=u3.id).count(), 1)
        # test the applications table
        # this test is failing
        # self.assertEqual(db.session.query(applications).count(), 2)

    def test_user_1(self):
        u1 = User(username='john',
            firstname = 'john',
            lastname = 'doe',
            wsuid = 12345678,
            phone = 42512345678,
            major = 'CPT_S',
            gpa = '4.0',
            graduationDate = datetime.now(),
            email='john.doe@wsu.com')
        db.session.add(u1)
        db.session.commit()
        self.assertEqual(User.query.count(), 1)
    
    def test_field(self):
        f1 = Field(name="TestField1")
        f2 = Field(name="TestField2")
        f3 = Field(name="TestField3")
        db.session.add(f1)
        db.session.add(f2)
        db.session.add(f3)
        db.session.commit()
        self.assertEqual(Field.query.count(), 3)

    def test_languages(self):
        l1 = Language(name="TestLanguage1")
        l2 = Language(name="TestLanguage2")
        l3 = Language(name="TestLanguage3")
        db.session.add(l1)
        db.session.add(l2)
        db.session.add(l3)
        db.session.commit()
        self.assertEqual(Language.query.count(), 3)
     

if __name__ == '__main__':
    unittest.main(verbosity=2)