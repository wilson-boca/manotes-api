from tests import base
from app.resource import resources


class TestNoteResource(base.TestCase):

    @base.TestCase.mock.patch('app.house.residents.User.get_a_note')
    def test_get_return_ok(self):
        note_resource = resources.NoteResource()
        note_resource.get(1)
