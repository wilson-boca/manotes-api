from tests import base
from mock import mock
from app.house import services, wall


class NoteServiceTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.wall.Note.create_new')
    def test_create(self, create_new_mock):
        services.NoteService.create({'key': 'value'})
        self.assertTrue(create_new_mock.called)

    @base.TestCase.mock.patch('app.house.wall.Note.list')
    def test_list(self, list_mock):
        services.NoteService.list()
        self.assertTrue(list_mock.called)

    @base.TestCase.mock.patch('app.house.wall.Note.delete_db')
    @base.TestCase.mock.patch('app.house.wall.Note.create_with_id')
    def test_delete(self, create_with_id_mock, delete_mock):
        create_with_id_mock.return_value = wall.Note(db_instance=mock.MagicMock())
        services.NoteService.delete(1)
        self.assertTrue(delete_mock.called)

    @base.TestCase.mock.patch('app.house.wall.Note.update')
    @base.TestCase.mock.patch('app.house.wall.Note.create_with_id')
    def test_update_by_id(self, create_with_id_mock, update_mock):
        create_with_id_mock.return_value = wall.Note(db_instance=mock.MagicMock())
        services.NoteService.update_by_id(1, {'i am': 'a python dict'})
        self.assertTrue(update_mock.called)
