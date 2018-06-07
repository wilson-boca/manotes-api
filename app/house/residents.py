from app.house import services


class User(object):

    class DeleteNoteError(Exception):
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
        except services.NoteService.DeleteError as ex:
            raise cls.DeleteNoteError(ex.message)

    @classmethod
    def get_a_note(cls, id):
        return services.NoteService.get_by_id(id)

    @classmethod
    def update_a_note(cls, id, note_json):
        return services.NoteService.update_by_id(id, note_json)
