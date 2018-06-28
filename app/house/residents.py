from app.house import services


class User(object):

    class NoteNotFound(Exception):
        pass

    class UserNotExists(Exception):
        pass


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
        except services.NoteService.NotFound as ex:
            raise cls.NoteNotFound(str(ex))

    @classmethod
    def get_a_note(cls, id):
        try:
            return services.NoteService.create_with_id(id)
        except services.NoteService.NotFound as ex:
            raise cls.NoteNotFound(str(ex))

    @classmethod
    def update_a_note(cls, id, note_json):
        try:
            return services.NoteService.update_by_id(id, note_json)
        except services.NoteService.NotFound as ex:
            raise cls.NoteNotFound(str(ex))