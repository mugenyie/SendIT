import unittest
import json
from api import app
from api.utils import string_generator
from .base import BaseTestCase


class SignUpAuthApiTestCase(BaseTestCase):

    # User signup tests

    def test_with_new_user(self):
        user = dict(
            email = string_generator(6) + '@gmail.com',
            username = string_generator(6),
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
        self.assertEqual(response.status_code, 400)


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
        self.assertEqual(response.status_code, 400)


    def test_email_is_invalid(self):
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
        self.assertEqual(response.status_code, 400)


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
        self.assertEqual(response.status_code, 400)

    
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
        self.assertEqual(response.status_code, 400)


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
        self.assertEqual(response.status_code, 400)


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
        self.assertEqual(response.status_code, 400)


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
        self.assertEqual(response.status_code, 400)