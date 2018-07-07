import json
from tests import base
from app.resource import resources
from app.house import residents


class NoteResourceTest(base.TestCase):

    @base.TestCase.mock.patch('app.resource.resources.g')
    def test_get_return_not_auth(self, g_mock):
        g_mock.authenticated = False
        note_resource = resources.NoteResource
        response = note_resource.get()
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.data), {"result": "Not Authorized"})

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_get_return_note_if_id(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = {'id': 1}
        logged_user_mock.get_a_note.return_value = note_mock
        note_resource = resources.NoteResource()
        response = note_resource.get(1)
        self.assertTrue(note_resource.me.get_a_note.called)
        self.assertEqual(response, {'id': 1})

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_get_return_not_mine(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = {'id': 1}
        logged_user_mock.get_a_note = self.mock.MagicMock(side_effect=residents.NotMine('foo'))
        note_resource = resources.NoteResource()
        response = note_resource.get(1)
        self.assertEqual(response[0], {'result': 'not-mine', 'error': 'Resource Not Mine', 'id': 1})

    @base.TestCase.mock.patch('app.resource.resources.g')
    @base.TestCase.mock.patch('app.resource.resources.NoteResource.logged_user')
    def test_get_return_not_found(self, logged_user_mock, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        note_mock = self.mock.MagicMock()
        note_mock.as_dict.return_value = {'id': 1}
        logged_user_mock.get_a_note = self.mock.MagicMock(side_effect=residents.NotFound('foo'))
        note_resource = resources.NoteResource()
        response = note_resource.get(1)
        self.assertEqual(response[0], {'result': 'not-found', 'error': 'Resource Not Found', 'id': 1})

    @base.TestCase.mock.patch('app.resource.resources.g')
    def test_get_call_query_if_not_note_id(self, g_mock):
        g_mock = self.mock.MagicMock()
        g_mock.authenticated.return_value = True
        note_resource = resources.NoteResource()
        note_resource.query = self.mock.MagicMock()
        note_resource.query.return_value = [{'id': 1}, {'id': 2}]
        response = note_resource.get()
        self.assertTrue(note_resource.query.called)
