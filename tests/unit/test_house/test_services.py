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

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_delete(self, note_mock):
        note_instance_mock = self.mock.MagicMock()
        note_mock.create_for_user.return_value = note_instance_mock
        note_instance_mock.delete.return_value = None
        services.NoteService.delete(1, 1)
        self.assertTrue(note_instance_mock.delete_db.called)

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_delete_raise_not_found(self, note_mock):
        note_instance_mock = self.mock.MagicMock()
        note_mock.create_for_user = self.mock.MagicMock(
            side_effect=services.NotFound('Could not find a note with id 1'))
        note_instance_mock.delete.return_value = None
        with self.assertRaises(services.NotFound):
            services.NoteService.delete(1, 1)

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_delete_raise_not_mine(self, note_mock):
        note_instance_mock = self.mock.MagicMock()
        note_mock.create_for_user = self.mock.MagicMock(
            side_effect=services.NotMine('Could not create note because it dont belong to user id 1'))
        note_instance_mock.delete.return_value = None
        with self.assertRaises(services.NotMine):
            services.NoteService.delete(1, 1)

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_update_by_id(self, note_mock):
        note_instance_mock = self.mock.MagicMock()
        note_mock.create_for_user.return_value = note_instance_mock
        note_instance_mock.update.return_value = None
        services.NoteService.update_by_id(1, {'i am': 'a python dict'}, 1)
        self.assertTrue(note_instance_mock.update.called)

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_update_by_id_raise_not_found(self, note_mock):
        note_instance_mock = self.mock.MagicMock()
        note_mock.create_for_user = self.mock.MagicMock(
            side_effect=services.NotFound('Could not find a note with id 1'))
        note_instance_mock.update.return_value = None
        with self.assertRaises(services.NotFound):
            services.NoteService.update_by_id(1, {'i am': 'a python dict'}, 1)

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_update_by_id_raise_not_mine(self, note_mock):
        note_instance_mock = self.mock.MagicMock()
        note_mock.create_for_user = self.mock.MagicMock(
            side_effect=services.NotMine('Could not create note because it dont belong to user id 1'))
        note_instance_mock.update.return_value = None
        with self.assertRaises(services.NotMine):
            services.NoteService.update_by_id(1, {'i am': 'a python dict'}, 1)
