import unittest
import json
from api import app
from random import randint
from .base import BaseTestCase


class SignUpAuthApiTestCase(BaseTestCase):

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

        response = self.client.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_registration_email_is_empty(self):
        user = dict(
            email = '' ,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.client.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_email_is_valid(self):
        user = dict(
            email = 'ecmugenyi' ,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.client.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_that_email_is_not_registered_already(self):
        user = dict(
            email = self.default_email,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.client.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_that_username_has_no_invalid_characters(self):
        user = dict(
            email = self.default_email,
            username = '*columbus',
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.client.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)

    
    def test_that_username_is_not_empty(self):
        user = dict(
            email = self.default_email,
            username = '',
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.client.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)

    
    def test_that_username_is_not_taken(self):
        user = dict(
            email = self.default_email,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.client.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_that_firstname_is_not_empty(self):
        user = dict(
            email = self.default_email,
            username = self.default_username,
            firstname = '',
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.client.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_that_lastname_is_not_empty(self):
        user = dict(
            email = self.default_email,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = '',
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.client.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_that_password_is_not_empty(self):
        user = dict(
            email = self.default_email,
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = ''
        )

        response = self.client.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_with_unregistered_user(self):
        user = dict(
            email = 'ec' + str(randint(0, 9)) + '@gmail.com',
            username = self.default_username,
            firstname = self.default_firstname,
            lastname = self.default_lastname,
            othernames = self.default_othernames,
            password = self.default_password
        )

        response = self.client.post(
            self.default_signup_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()