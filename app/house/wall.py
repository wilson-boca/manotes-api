import datetime
from app import config
from app import models

config = config.get_config()


class NotFound(Exception):
    pass


class NotMine(Exception):
    pass


class Note(object):
    repository = models.Note

    def __init__(self, db_instance):
        self.db_instance = db_instance
        self.id = db_instance.id
        self.color = db_instance.color

    @property
    def name(self):
        return self.db_instance.name

    @property
    def content(self):
        return self.db_instance.content

    @classmethod
    def create_with_id(cls, note_id):
        db_instance = cls.repository.one_or_none(id=note_id)
        if db_instance is None:
            raise NotFound('Could not find a note with id {}'.format(note_id))
        return cls(db_instance=db_instance)

    @classmethod
    def create_for_user(cls, id, user_id):
        db_instance = cls.repository.one_or_none(id=id)
        if db_instance is None:
            raise NotFound('Could not find a note with id {}'.format(id))
        if db_instance.user_id != user_id:
            raise NotMine('Could not create note because it dont belong to user id {}'.format(user_id))
        return cls(db_instance=db_instance)

    @classmethod
    def create_with_instance(cls, db_instance):
        return cls(db_instance)

    @classmethod
    def create_new(cls, note_json):
        cls.repository.create_from_json(note_json)

    @classmethod
    def list_for_user(cls, user_id):
        notes_db = cls.repository.filter(user_id=user_id)
        notes = [cls.create_with_instance(note_db) for note_db in notes_db]
        return notes

    def update(self, note_json):
        note_json['update_date'] = datetime.datetime.utcnow()
        return self.db_instance.update_from_json(note_json)

    def delete_db(self):
        self.db_instance.delete_db()

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'color': self.color
        }