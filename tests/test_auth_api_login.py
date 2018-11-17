import unittest
import json
from api import app
from random import randint
from utils import string_generator
from .base import BaseTestCase


class LoginAuthApiTestCase(BaseTestCase):


    # User login tests

    def test_that_password_is_not_empty(self):
        user = dict(
            username = self.default_username,
            password = ''
        )
        response = self.client.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )
        self.assertEqual(response.status_code, 400)


    def test_with_empty_username(self):
        user = dict(
            username = '',
            password = self.default_password
        )
        response = self.client.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )
        self.assertEqual(response.status_code, 400)


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
        self.assertEqual(response.status_code, 400)


    def test_that_username_has_no_invalid_characters(self):
        user = dict(
            username = '*columbus',
            password = self.default_password
        )
        response = self.client.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )
        self.assertEqual(response.status_code, 400)

    def test_with_inexistent_user(self):
        user = dict(
            username = string_generator(6),
            password = string_generator(6)
        )
        response = self.client.post(
            self.default_login_endpoint,
            content_type='application/json',
            data=json.dumps(user)
        )
        self.assertEqual(response.status_code, 404)
    