# -*- coding: utf-8 -*-
from app import config as config_module

from app import database

db = database.AppRepository.db

config = config_module.get_config()


class AbstractModel(object):
    class AlreadyExist(Exception):
        pass

    class NotExist(Exception):
        pass

    class RepositoryError(Exception):
        pass

    @classmethod
    def one_or_none(cls, **kwargs):
        return cls.filter(**kwargs).one_or_none()

    @classmethod
    def filter(cls, **kwargs):
        return cls.query.filter_by(**kwargs)

    def save_db(self, commit=True):
        db.session.add(self)
        if commit:
            db.session.commit()
        else:
            db.session.flush()

    def delete_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def create_from_json(cls, json_data):
        try:
            instance = cls()
            instance.set_values(json_data)
            instance.save_db()
            return instance
        except Exception as ex:
            raise cls.RepositoryError(str(ex))

    def update_from_json(self, json_data):
        try:
            self.set_values(json_data)
            self.save_db()
            return self
        except Exception as ex:
            raise self.RepositoryError(str(ex))

    def set_values(self, json_data):
        for key, value in json_data.items():
            setattr(self, key, json_data.get(key, getattr(self, key))) # WTF


class Note(db.Model, AbstractModel):
    __tablename__ = 'manotes_notes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    content = db.Column(db.String)
    color = db.Column(db.String)


class User(db.Model, AbstractModel):
    __tablename__ = 'manotes_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    email = db.Column(db.String, unique=True)
    token = db.Column(db.String, unique=True)
    password = db.Column(db.String)
