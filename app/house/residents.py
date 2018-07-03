from app.house import services
from app import models


class NotFound(Exception):
    pass


class NotExists(Exception):
    pass


class User(object):
    repository = models.User

    def __init__(self, db_instance):
        self.db_instance = db_instance
        self.id = db_instance.id

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
            raise NotFound('Could not find a note with id {}'.format(id))
        return cls(db_instance=db_instance)

    @classmethod
    def create_with_instance(cls, db_instance):
        return cls(db_instance)

    @classmethod
    def create_with_token(cls, token):
        db_instance = cls.repository.one_or_none(token=token)
        if db_instance is None:
            raise NotFound('Could not find a user with token {}'.format(token))
        return cls(db_instance=db_instance)

    @classmethod
    def create_with_username(cls, username):
        db_instance = cls.repository.one_or_none(username=username)
        if db_instance is None:
            raise NotFound('Could not find a user with username {}'.format(username))
        return cls(db_instance=db_instance)

    @classmethod
    def create_a_note(cls, note_json):
        services.NoteService.create(note_json)

    @classmethod
    def list_notes(cls):
        return services.NoteService.list()

    @classmethod
    def delete_a_note(cls, id):
        try:
            return services.NoteService.delete(id)
        except services.NotFound as ex:
            raise NotFound(str(ex))

    @classmethod
    def get_a_note(cls, id):
        try:
            return services.NoteService.create_with_id(id)
        except services.NotFound as ex:
            raise NotFound(str(ex))

    @classmethod
    def update_a_note(cls, id, note_json):
        try:
            return services.NoteService.update_by_id(id, note_json)
        except services.NotFound as ex:
            raise NotFound(str(ex))
