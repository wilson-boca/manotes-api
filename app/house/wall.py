import datetime
from app import config, models, exceptions
from app.base import domain

config = config.get_config()


class Note(domain.Entity):
    repository = models.Note

    def __init__(self, db_instance):
        super(Note, self).__init__(db_instance)
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
    def create_for_user(cls, id, user_id):
        db_instance = cls.repository.one_or_none(id=id)
        if db_instance is None:
            raise exceptions.NotFound('Could not find a note with id {}'.format(id))
        if db_instance.user_id != user_id:
            raise exceptions.NotMine('Could not create note because it dont belong to user id {}'.format(user_id))
        return cls(db_instance=db_instance)

    @classmethod
    def create_new(cls, note):
        db_instance = cls.repository.create_from_dict(note)
        return cls.create_with_instance(db_instance)

    @classmethod
    def list_for_user(cls, user_id):
        db_instances = cls.repository.filter(user_id=user_id)
        notes = [cls.create_with_instance(db_instance) for db_instance in db_instances]
        return notes

    def update(self, note):
        note['update_date'] = datetime.datetime.utcnow()
        self.db_instance.update_from_dict(note)

    def delete(self):
        self.db_instance.delete_db()

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'color': self.color
        }
