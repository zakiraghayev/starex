from django.test import TestCase, Client

# Create your tests here.
class HomeTest(TestCase):

    def test_get_home_page(self):
        """ testing home page found. """
        c = Client()
        res = c.get('/')
        self.assertEqual(res.status_code, 200)