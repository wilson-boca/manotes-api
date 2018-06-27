from tests import base
from app.house import services


class NoteServiceTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.wall.Note.create_new')
    def test_create(self, create_new_mock):
        services.NoteService.create({'key': 'value'})
        self.assertTrue(create_new_mock.called)

    @base.TestCase.mock.patch('app.house.wall.Note.list')
    def test_list(self, list_mock):
        services.NoteService.list()
        self.assertTrue(list_mock.called)

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_delete(self, note_mock):
        note_instance_mock = self.mock.MagicMock()
        note_mock.create_with_id.return_value = note_instance_mock
        note_instance_mock.delete.return_value = None
        services.NoteService.delete(1)
        self.assertTrue(note_instance_mock.delete_db.called)

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_update_by_id(self, note_mock):
        note_instance_mock = self.mock.MagicMock()
        note_mock.create_with_id.return_value = note_instance_mock
        note_instance_mock.update.return_value = None
        services.NoteService.update_by_id(1, {'i am': 'a python dict'})
        self.assertTrue(note_instance_mock.update.called)
