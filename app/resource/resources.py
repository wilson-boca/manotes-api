import re
from functools import wraps
from flask_restful import Resource
from flask import g, Response, request
from app.house import residents


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authenticated = getattr(g, 'authenticated', False)
        if not authenticated:
            return Response('{"result": "Not Authorized"}', 401, content_type='application/json')
        return f(*args, **kwargs)

    return decorated_function


def not_allowed(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        return Response('{"result": "Method not allowed"}', 405, content_type='application/json')
    return decorated_function

class ResourceBase(Resource):

    @property
    def payload(self):
        payload = {}
        if request.json:
            payload.update(self.transform_key(request.json, self.camel_to_snake))
        if request.form:
            payload.update(self.transform_key(request.form, self.camel_to_snake))
        if request.args:
            payload.update(self.transform_key(request.args, self.camel_to_snake))
        return payload

    @staticmethod
    def camel_to_snake(name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    @staticmethod
    def snake_to_camel(name):
        result = []
        for index, part in enumerate(name.split('_')):
            if index == 0:
                result.append(part.lower())
            else:
                result.append(part.capitalize())
        return ''.join(result)

    def transform_key(self, data, method):
        if isinstance(data, dict):
            return {method(key): self.transform_key(value, method) for key, value in data.items()}
        if isinstance(data, list):
            for index, item in enumerate(data):
                if isinstance(item, dict):
                    data[index] = {method(key): self.transform_key(value, method) for key, value in item.items()}
        return data

    def response(self, data_dict):
        return self.transform_key(data_dict, self.snake_to_camel)

    def return_unexpected_error(self):
        return {'result': 'error', 'error': 'Internal Server Error', 'exception': 'An unexpected error occurred'}, 500

    def return_ok(self, **extra):
        result = {'result': 'OK'}
        if extra is not None:
            result.update(extra)
        return result

    def return_not_found(self, **extra):
        result = {'result': 'not-found', 'error': 'Resource Not Found'}
        if extra is not None:
            result.update(extra)
        return result, 404


class LoginResource(ResourceBase):
    entity = residents.EnemDoorman

    @not_allowed
    def get(self):
        pass

    def post(self):
        try:
            if self.entity.authenticate(self.payload):
                g.user = self.entity
                g.current_token = 'MoCkEdToKeN'
                return {'result': 'OK'}, 200
            else:
                return {'result': 'Not Authorized'}, 401
        except self.entity.UserNotExists as ex:
            return {'result': 'not-found', 'error': 'Resource Not Found'}
        except Exception as ex:
            return {'result': 'Not Authorized'}, 401

    @not_allowed
    def put(self):
        pass

    @not_allowed
    def delete(self):
        pass


class NoteResource(ResourceBase):
        me = residents.User

        def query(self):
            notes = self.me.list_notes()
            return self.response([note.as_dict() for note in notes])

        def get(self, note_id=None):
            if note_id is None:
                return self.query()

            try:
                note = self.me.get_a_note(note_id)
                return note.as_dict()
            except self.me.NoteNotFound as ex:
                return self.return_not_found()
            except Exception as ex:
                return self.return_unexpected_error()

        def post(self):
            self.me.create_a_note(self.payload)
            return self.return_ok()

        def put(self, note_id):
            try:
                self.me.update_a_note(note_id, self.payload)
                return self.return_ok()
            except self.me.NoteNotFound as ex:
                return self.return_not_found()
            except Exception as ex:
                return self.return_unexpected_error()

        def delete(self, note_id):
            try:
                self.me.delete_a_note(note_id)
                return self.return_ok()
            except self.me.NoteNotFound as ex:
                return self.return_not_found()
            except Exception as ex:
                return self.return_unexpected_error()
