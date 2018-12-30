# -*- coding: utf-8 -*-
import secrets
from importlib import import_module
from passlib.hash import pbkdf2_sha256


class ClassProperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


def classproperty(func):
    return ClassProperty(func)


class Service(object):
    _entity = None

    class InvalidDomain(Exception):
        pass

    @classproperty
    def entity(cls):
        if cls._entity is None:
            raise cls.InvalidDomain('You should use a specific service implementation')
        try:
            return import_module(cls._entity)
        except Exception as ex:
            pass


class HashService(Service):

    @classmethod
    def hash(cls, word):
        return pbkdf2_sha256.hash(word)

    @classmethod
    def is_string_equals_to_hash(cls, string, hashed_string):
        return pbkdf2_sha256.verify(string, hashed_string)


class TokenService(Service):

    @classmethod
    def generate_a_token(cls):
        return secrets.token_hex(40)
