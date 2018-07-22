from flask_restful import Api
from app.resource import resources


def create_api(app):
    api = Api(app)
    api.add_resource(resources.NoteResource, '/api/notes', '/api/notes/<int:note_id>')
    api.add_resource(resources.AccountResource, '/api/account')
    api.add_resource(resources.LoginResource, '/api/login')
