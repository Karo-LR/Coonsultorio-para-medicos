from django.test import TestCase

class BasicTest(TestCase):
    def test_api(self):
        self.assertEqual(1, 1)