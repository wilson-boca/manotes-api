from flask_restful import Api


def create_api(app):
    from app.resource import resources

    api = Api(app)
    api.add_resource(resources.NoteResource, '/api/notes', '/api/notes/<int:note_id>')
