import datetime
import secrets
import io
import os
from passlib.hash import pbkdf2_sha256
from app.house import services
from app.async_tasks import tasks
from app import models, exceptions, config as config_module

config = config_module.get_config()


class AbstractUser(object):
    repository = models.User


class User(AbstractUser):

    def __init__(self, db_instance):
        self.db_instance = db_instance
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

    @classmethod
    def create_with_id(cls, id):
        db_instance = cls.repository.one_or_none(id=id)
        if db_instance is None:
            raise exceptions.NotFound('Could not find a note with id {}'.format(id))
        return cls(db_instance=db_instance)

    @classmethod
    def create_with_instance(cls, db_instance):
        return cls(db_instance)

    @classmethod
    def create_with_token(cls, token):
        db_instance = cls.repository.one_or_none(token=token)
        if db_instance is None:
            raise exceptions.NotFound('Could not find a user with token {}'.format(token))
        return cls(db_instance=db_instance)

    @classmethod
    def create_with_username(cls, username):
        db_instance = cls.repository.one_or_none(username=username)
        if db_instance is None:
            raise exceptions.NotFound('Could not find a user with username {}'.format(username))
        return cls(db_instance=db_instance)

    def create_a_note(self, note_json):
        note_json['user_id'] = self.id
        services.NoteService.create_new(note_json)

    def delete_a_note(self, id):
        services.NoteService.delete(id, self.id)

    def get_a_note(self, id):
        return services.NoteService.create_for_user(id, self.id)

    def update_a_note(self, id, note_json):
        return services.NoteService.update_by_id(id, note_json, self.id)

    def update(self, payload):
        payload.pop('password', None)
        payload['update_date'] = datetime.datetime.utcnow()
        self.db_instance.update_from_json(payload)

    def change_avatar(self, files):
        try:
            avatar_file = files['avatar']
            temp_file_path = '{}/{}-{}'.format(config.TEMP_PATH, self.id, 'avatar.png')
            avatar_file.save(temp_file_path)

            file_path_to_save = services.AvatarFilePath.bring_file_path_to_save(self.id)

            services.FileService.save(temp_file_path, file_path_to_save, self.id)
        except Exception as ex:
            pass


class UnknowUser(AbstractUser):

    @classmethod
    def create_account(cls, payload):
        payload['password'] = pbkdf2_sha256.hash(payload['password'])
        payload['token'] = secrets.token_hex(40)
        user = cls.repository.create_from_json(payload)
        name = user.username
        from_address = "antunesleo4@gmail.com"
        to_address = user.email
        subject = "Test"

        tasks.start_send_email(name, from_address, to_address, subject)
