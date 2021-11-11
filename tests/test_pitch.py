import unittest
from app.models import Pitch


class TestPitch(unittest.TestCase):
    def setUp(self):
        self.new_pitch = Pitch(title="Test Pitch Title",
                             body="Test Content body", author_id="Test Pitch Author", slug="test-pitch-slug")

    def test_instance(self):
        self.assertTrue(isinstance(self.new_pitch, Pitch))