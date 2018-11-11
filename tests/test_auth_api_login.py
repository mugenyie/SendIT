import unittest
import json
from api import app
from random import randint
from .base import BaseTestCase


class LoginAuthApiTestCase(BaseTestCase):


    # User login tests
    def test_login_email_with_space(self):
        user = dict(
            email = ' ' ,
            password = self.default_password
        )

        response = self.client.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_login_with_empty_email(self):
        user = dict(
            email = '' ,
            password = self.default_password
        )

        response = self.client.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_that_email_is_valid(self):
        user = dict(
            email = 'ecmugenyi',
            password = self.default_password
        )

        response = self.client.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_that_password_is_not_empty(self):
        user = dict(
            email = self.default_email,
            password = ''
        )

        response = self.client.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_that_username_is_not_empty(self):
        user = dict(
            username = '',
            password = self.default_password
        )

        response = self.client.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_that_username_is_not_space(self):
        user = dict(
            username = ' ',
            password = self.default_password
        )

        response = self.client.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_that_username_has_no_invalid_characters(self):
        user = dict(
            email = '*columbus',
            password = self.default_password
        )

        response = self.client.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 404)


    def test_with_registered_user(self):
        user = dict(
            email = self.default_email,
            password = self.default_password
        )

        response = self.client.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )

        self.assertEqual(response.status_code, 200)