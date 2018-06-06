# -*- coding: utf-8 -*-
from importlib import import_module


class classproperty(object):
    def __init__(self, getter):
        self.getter = getter

    def __get__(self, instance, owner):
        return self.getter(owner)


class Service(object):
    _entity = None

    class InvalidDomain(Exception):
        pass

    def __init__(self):
        self.domain()

    @classproperty
    def entity(cls):
        if cls._entity is None:
            raise cls.InvalidDomain('You should use a specific service implementation')
        try:
            return import_module(cls._entity)
        except Exception as ex:
            pass


class NoteService(Service):
    _entity = 'app.entities'

    @classmethod
    def create_a_note_for_user(cls, note_json):
        cls.entity.Note.create_new(note_json)

    @classmethod
    def list_notes_for_user(cls):
        return cls.entity.Note.list_for_user()

    @classmethod
    def delete_a_note_for_user(cls, id):
        note = cls.entity.Note.create_with_id(id)
        return note.delete_db()

    @classmethod
    def get_a_note_for_user(cls, id):
        return cls.entity.Note.get_note_for_user(id)

    @classmethod
    def update_a_note_for_user(cls, id, note_json):
        note = cls.entity.Note.create_with_id(id)
        return note.update_note_for_user(note_json)
