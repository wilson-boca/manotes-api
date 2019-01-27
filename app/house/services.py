# -*- coding: utf-8 -*-
from app.base.services import Service
from app.central_files import archive
from app.house import residents


class NoteService(Service):
    _entity = 'app.house.wall'

    @classmethod
    def create_new(cls, note):
        return cls.entity.Note.create_new(note)

    @classmethod
    def list_for_user(cls, user_id):
        return cls.entity.Note.list_for_user(user_id)

    @classmethod
    def create_for_user(cls, id, user_id):
        return cls.entity.Note.create_for_user(id, user_id)

    @classmethod
    def update_by_id(cls, id, changed_note, user_id):
        note = cls.entity.Note.create_for_user(id, user_id)
        note.update(changed_note)
        return note


class FileService(Service):

    @classmethod
    def save_avatar(cls, temp_file_path, user_id):
        file = archive.ScribeFactory.create_with_environment(user_id, router='avatar')
        return file.save(temp_file_path)


class UserService(Service):

    @classmethod
    def create_new(cls, user):
        return residents.User.create_new(user)
