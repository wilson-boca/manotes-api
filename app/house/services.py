# -*- coding: utf-8 -*-
import secrets
from importlib import import_module
from passlib.hash import pbkdf2_sha256
from app.files_drawer import drawer


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


class NoteService(Service):
    _entity = 'app.house.wall'

    @classmethod
    def create_new(cls, note_json):
        return cls.entity.Note.create_new(note_json)

    @classmethod
    def list_for_user(cls, user_id):
        return cls.entity.Note.list_for_user(user_id)

    @classmethod
    def create_for_user(cls, id, user_id):
        return cls.entity.Note.create_for_user(id, user_id)

    @classmethod
    def update_by_id(cls, id, note_json, user_id):
        note = cls.entity.Note.create_for_user(id, user_id)
        note.update(note_json)
        return note


class FileService(Service):

    @classmethod
    def save_avatar(cls, temp_file_path, user_id):
        file = drawer.File.create_with_environment(user_id, router='avatar')
        return file.save(temp_file_path)


class SecurityService(Service):

    @classmethod
    def generate_a_token(cls):
        return secrets.token_hex(40)

    @classmethod
    def hash(cls, word):
        return pbkdf2_sha256.hash(word)

    @classmethod
    def is_string_equals_to_hash(cls, string, hashed_string):
        return pbkdf2_sha256.verify(string, hashed_string)
