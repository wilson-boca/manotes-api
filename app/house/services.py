# -*- coding: utf-8 -*-
from importlib import import_module


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

    class DeleteError(Exception):
        pass

    class NotFound(Exception):
        pass

    @classmethod
    def create(cls, note_json):
        cls.entity.Note.create_new(note_json)

    @classmethod
    def list(cls):
        return cls.entity.Note.list()

    @classmethod
    def delete(cls, id):
        try:
            note = cls.entity.Note.create_with_id(id)
            return note.delete_db()
        except cls.entity.Note.NotFound as ex:
            raise cls.NotFound(str(ex))

    @classmethod
    def create_with_id(cls, id):
        try:
            return cls.entity.Note.create_with_id(id)
        except cls.entity.Note.NotFound as ex:
            raise cls.NotFound(str(ex))

    @classmethod
    def update_by_id(cls, id, note_json):
        try:
            note = cls.entity.Note.create_with_id(id)
            return note.update(note_json)
        except cls.entity.Note.NotFound as ex:
            raise cls.NotFound(str(ex))
