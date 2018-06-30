# -*- coding: utf-8 -*-
from app.house import residents


class AuthService(object):

    class UserNotExists(Exception):
        pass

    @classmethod
    def authenticate(cls, credentials):
        if credentials['username'] == 'breno':
            if credentials['password'] == '12345':
                return True
            return False
        raise cls.UserNotExists('The user {} not exists')

    @classmethod
    def authenticate_token(cls, token):
        authenticated = False
        if token == 'MoCkEdToKeN':
            authenticated = True
            return authenticated, residents.User.create_with_token(token)
        return authenticated, None
