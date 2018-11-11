import unittest
from api import app


class BaseTestCase(unittest.TestCase):

    default_login_endpoint = 'api/v1/auth/login'
    default_signup_endpoint = 'api/v1/auth/signup'
    default_email = 'ecmugenyi@gmail.com'
    default_username = 'columbus'
    default_password = '1234'
    default_firstname = 'Emmanuel'
    default_lastname = 'Mugenyi'
    default_othernames = 'Columbus'
    
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        # method to invoke after each test.
        pass