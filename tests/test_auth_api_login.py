import unittest
import json
from api import app


class TestApiEndPoints(unittest.TestCase):
    default_login_endpoint = 'api/v1/auth/login'
    default_email = 'ecmugenyi@gmail.com'
    default_username = 'columbus'
    default_password = '1234'

    def setUp(self):
        self.tester = app.test_client(self)

    # User login tests
    def test_registration_email_with_space(self):
        user = dict(
            email = ' ' ,
            password = self.default_password
        )

        response = self.tester.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Sorry, enter your email!")

    def test_registration_with_empty_email(self):
        user = dict(
            email = '' ,
            password = self.default_password
        )

        response = self.tester.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Sorry, enter your email!")

    def test_that_email_is_already_registered(self):
        user = dict(
            email = self.default_email,
            password = self.default_password
        )

        response = self.tester.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Sorry, email already registered with another user!")

    def test_that_email_is_valid(self):
        user = dict(
            email = 'ecmugenyi',
            password = self.default_password
        )

        response = self.tester.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        reply = json.loads(response.data.decode())
        self.assertEqual(reply["data"], "Sorry, email already registered with another user!")

    def test_that_password_is_not_empty(self):
            user = dict(
                email = self.email,
                password = ''
            )

            response = self.tester.post(
                self.default_login_endpoint,
                content_type='application/json',
                data=json.dumps(user)
            )

            reply = json.loads(response.data.decode())
            self.assertEqual(reply["data"], "Sorry, password can not be empty!")

    def test_that_username_is_not_empty(self):
            user = dict(
                username = '',
                password = self.default_password
            )

            response = self.tester.post(
                self.default_login_endpoint,
                content_type='application/json',
                data=json.dumps(user)
            )

            reply = json.loads(response.data.decode())
            self.assertEqual(reply["data"], "Sorry, username can not be empty!")

    def test_that_username_is_not_space(self):
            user = dict(
                username = ' ',
                password = self.default_password
            )

            response = self.tester.post(
                self.default_login_endpoint,
                content_type='application/json',
                data=json.dumps(user)
            )

            reply = json.loads(response.data.decode())
            self.assertEqual(reply["data"], "Sorry, username should not contain a space!")

    def test_that_username_has_no_invalid_characters(self):
            user = dict(
                email = '*columbus',
                password = self.default_password
            )

            response = self.tester.post(
                self.default_login_endpoint,
                content_type='application/json',
                data=json.dumps(user)
            )

            reply = json.loads(response.data.decode())
            self.assertEqual(reply["data"], "Sorry, username should contain valid characters!")