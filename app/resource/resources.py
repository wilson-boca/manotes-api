import re
from flask_restful import Resource, request
from app import entities


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


class NoteResource(ResourceBase):
        me = entities.User

        def query(self):
            notes = self.me.list_notes()
            return self.response([note.as_dict() for note in notes])

        def get(self, note_id=None):
            if note_id is None:
                return self.query()
            note = self.me.get_a_note(note_id)
            return note.as_dict()

        def post(self):
            self.me.create_a_note(self.payload)
            return self.return_ok()

        def put(self, note_id):
            self.me.update_a_note(note_id, self.payload)
            return self.return_ok()

        def delete(self, note_id):
            try:
                self.me.delete_a_note(note_id)
                return self.return_ok()
            except Exception as ex:
                pass