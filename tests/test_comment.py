import unittest
from app.models import Comment
from app import db

class CommentModelTest(unittest.TestCase):
    def setUp(self):
        self.new_comment = Comment(description = 'content')
        db.session.add(self.new_comment)
        db.session.commit()
        
    def tearDown(self):
        Comment.query.delete()
        db.session.commit()

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.description, 'content')

    def tearDown(self):
        Comment.query.delete()
        db.session.commit()

    def test_save_comment(self):
        self.new_comment.save_comment()
        self.assertTrue(len(Comment.query.all())>0)

    def test_check_instance_variables(self):
        self.assertEquals(self.new_comment.description, 'content')