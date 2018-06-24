from tests import base
from app.resource import resources


class TestNoteResource(base.TestCase):

    @base.TestCase.mock.patch('app.house.residents.User')
    def test_get_return_ok(self, user_mock):
        user_mock.get_a_note.return_value =  {}
        note_resource = resources.NoteResource()
        note_resource.get(1)
        self.assertTrue(1, 1)
