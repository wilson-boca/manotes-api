# -*- coding: utf-8 -*-
from passlib.hash import pbkdf2_sha256
from flask import g
from app import exceptions


class AuthService(object):

    @classmethod
    def authenticate_with_credentials(cls, credentials):
        from app.house import residents, services
        try:
            user = residents.User.create_with_username(credentials['username'])
        except exceptions.NotFound:
            raise exceptions.UserNotExists('Could not find a user with username {}'.format(credentials['username']))
        return services.EncryptionService.is_equal(credentials['password'], user.password), user

    @classmethod
    def authenticate_with_token(cls, token):
        from app.house import residents
        try:
            user = residents.User.create_with_token(token)
            g.user = user
            g.current_token = user.token
            g.authenticated = True
        except exceptions.NotFound:
            g.authenticated = False
