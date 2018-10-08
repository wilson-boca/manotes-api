from tests import base
from app.house import services


class NoteServiceTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_create(self, note_mock):
        note_mock.create_new = self.mock.MagicMock(return_value=None)
        services.NoteService.create_new({'key': 'value'})
        self.assertTrue(note_mock.create_new.called)

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_list(self, note_mock):
        note_mock.list_for_user = self.mock.MagicMock(return_value=None)
        services.NoteService.list_for_user(1)
        self.assertTrue(note_mock.list_for_user.called)
