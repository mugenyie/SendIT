import unittest
import json
from api import app


class TestApiEndPoints(unittest.TestCase):
    default_signup_endpoint = 'api/v1/auth/signup'
    default_email = 'ecmugenyi@gmail.com'
    default_username = 'columbus'
    default_password = '1234'
    default_firstname = 'Emmanuel'
    default_lastname = 'Mugenyi'
    default_othernames = 'Columbus'

    def setUp(self):
        self.tester = app.test_client(self)

    # User signup tests

    def test_registration_email_with_space(self):
        user = dict(
            email = ' ' ,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.tester.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Email contain space!")


    def test_registration_email_is_empty(self):
        user = dict(
            email = '' ,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.tester.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Email can not be empty!")


    def test_email_is_valid(self):
        user = dict(
            email = 'ecmugenyi' ,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.tester.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Email is invalid!")


    def test_that_email_is_not_registered_already(self):
        user = dict(
            email = self.default_email,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.tester.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Sorry, use with similar email already registered!")


    def test_that_username_has_no_invalid_characters(self):
        user = dict(
            email = self.default_email,
            username = '*columbus',
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.tester.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Sorry, username contains invalid characters!")

    
    def test_that_username_is_not_empty(self):
        user = dict(
            email = self.default_email,
            username = '',
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.tester.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Sorry, username should not be empty!")

    
    def test_that_username_is_not_taken(self):
        user = dict(
            email = self.default_email,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.tester.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Sorry, username alreday taken!")


    def test_that_firstname_is_not_empty(self):
        user = dict(
            email = self.default_email,
            username = self.default_username,
            firstname = '',
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.tester.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Sorry, firstname should not be empty!")

    def test_that_lastname_is_not_empty(self):
        user = dict(
            email = self.default_email,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = '',
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.tester.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Sorry, lastname should not be empty!")


    def test_that_password_is_not_empty(self):
        user = dict(
            email = self.default_email,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = ''
        )

        response = self.tester.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Sorry, password should not be empty!")

    def test_with_correct_details(self):
        user = dict(
            email = 'mugenyie@gmail.com',
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.tester.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Sorry, password should not be empty!")

    