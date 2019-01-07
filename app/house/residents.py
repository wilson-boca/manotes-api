import datetime
from app.house import services
from app import models, exceptions, config as config_module

config = config_module.get_config()


class User(object):
    repository = models.User

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

    @classmethod
    def create_with_email(cls, email):
        db_instance = cls.repository.one_or_none(email=email)
        if db_instance is None:
            raise exceptions.NotFound('Could not find a user with email {}'.format(email))
        return cls(db_instance=db_instance)

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
