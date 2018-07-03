# -*- coding: utf-8 -*-
from passlib.hash import pbkdf2_sha256


class AuthService(object):

    class UserNotExists(Exception):
        pass

    @classmethod
    def authenticate(cls, credentials):
        from app.house import residents, services
        try:
            user = residents.User.create_with_username(credentials['username'])
        except residents.User.NotFound:
            raise cls.UserNotExists('Could not find a user with username {}'.format(credentials['username']))
        return services.EncryptionService.is_equal(credentials['password'], user.password), user

    @classmethod
    def authenticate_token(cls, token):
        from app.house import residents
        # authenticated = False
        # if token == 'MoCkEdToKeN':
        #     authenticated = True
        #     return authenticated, residents.User.create_with_token(token)
        # return authenticated, None
        try:
            return residents.User.create_with_token(token)
        except residents.User.NotFound:
            raise cls.UserNotExists('Could not find a user with token {}'.format(token))
