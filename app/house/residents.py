# -*- coding: utf-8 -*-
import datetime
from app.house import services
from app.base import domain
from app import models, config as config_module

config = config_module.get_config()


class User(domain.Entity):
    repository = models.User

    def __init__(self, db_instance):
        super(User, self).__init__(db_instance)
        self.id = db_instance.id
        self._notes = None

    @property
    def notes(self):
        if self._notes is None:
            self._notes = services.NoteService.list_for_user(user_id=self.id)
        return self._notes

    @property
    def token(self):
        return self.db_instance.token

    @property
    def password(self):
        return self.db_instance.password

    @property
    def username(self):
        return self.db_instance.username

    @property
    def email(self):
        return self.db_instance.email

    @property
    def avatar_path(self):
        return self.db_instance.avatar_path

    @classmethod
    def create_with_token(cls, token):
        return cls._create_with_keys(token=token)

    @classmethod
    def create_with_username(cls, username):
        return cls._create_with_keys(username=username)

    @classmethod
    def create_with_email(cls, email):
        return cls._create_with_keys(email=email)

    # TODO: Isso está errado? Deveria o clerk ter esse repositório e salvar?
    @classmethod
    def create_new(cls, user):
        car = cls.repository.create_from_dict(user)
        return cls.create_with_instance(car)

    def create_a_note(self, note):
        note['user_id'] = self.id
        return services.NoteService.create_new(note)

    def delete_a_note(self, id):
        note = services.NoteService.create_for_user(id, self.id)
        note.delete()

    def get_a_note(self, id):
        return services.NoteService.create_for_user(id, self.id)

    def update_a_note(self, id, note_changes):
        note = services.NoteService.create_for_user(id, self.id)
        note.update(note_changes)
        return note

    def update(self, payload):
        payload.pop('password', None)
        payload['update_date'] = datetime.datetime.utcnow()
        self.db_instance.update_from_dict(payload)

    def change_avatar(self, files):
        avatar_file = files['avatar']
        temp_file_path = '{}/{}-{}'.format(config.TEMP_PATH, self.id, 'avatar.png')
        avatar_file.save(temp_file_path)
        image_path = services.FileService.save_avatar(temp_file_path, self.id)
        self.db_instance.avatar_path = image_path
        self.db_instance.save_db()

    def as_dict(self):
        return {
            "username": self.db_instance.username,
            "email": self.db_instance.email
        }
