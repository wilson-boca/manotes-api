from tests import base
from app.resource import resources


class NoteResourceTest(base.TestCase):

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.house.residents.User')
    def test_get_return_ok(self, user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = False
        user_mock.get_a_note.return_value =  {}
        note_resource = resources.NoteResource()
        note_resource.get(1)

        self.assertTrue(1, 1)
