# -*- coding: utf-8 -*-
from importlib import import_module
from passlib.hash import pbkdf2_sha256
from app.house import wall, residents


class ClassProperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


def classproperty(func):
    return ClassProperty(func)


class DeleteError(Exception):
    pass


class NotFound(Exception):
    pass


class NotMine(Exception):
    pass


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
        cls.entity.Note.create_new(note_json)

    @classmethod
    def list_for_user(cls, user_id):
        return cls.entity.Note.list_for_user(user_id)

    @classmethod
    def delete(cls, id, user_id):
        try:
            note = cls.entity.Note.create_for_user(id, user_id)
            return note.delete_db()
        except wall.NotFound as ex:
            raise NotFound(str(ex))
        except wall.NotMine as ex:
            raise NotMine(str(ex))

    @classmethod
    def create_for_user(cls, id, user_id):
        try:
            return cls.entity.Note.create_for_user(id, user_id)
        except wall.NotFound as ex:
            raise NotFound(str(ex))
        except wall.NotMine as ex:
            raise NotMine(str(ex))

    @classmethod
    def update_by_id(cls, id, note_json, user_id):
        try:
            note = cls.entity.Note.create_for_user(id, user_id)
            return note.update(note_json)
        except wall.NotFound as ex:
            raise NotFound(str(ex))
        except wall.NotMine as ex:
            raise NotMine(str(ex))


class EncryptionService(Service):

    @classmethod
    def is_equal(cls, string, hashed_string):
        return pbkdf2_sha256.verify(string, hashed_string)
