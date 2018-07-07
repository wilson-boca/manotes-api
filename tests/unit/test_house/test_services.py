from tests import base
from app.house import services


class NoteServiceTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.wall.Note.create_new')
    def test_create(self, create_new_mock):
        services.NoteService.create_new({'key': 'value'})
        self.assertTrue(create_new_mock.called)

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_create_not_found(self, note_mock):
        note_mock.create_new = self.mock.MagicMock(side_effect=services.NotFound('foo'))
        with self.assertRaises(services.NotFound):
            services.NoteService.create_new({'key': 'value'})

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_create_not_mine(self, note_mock):
        note_mock.create_new = self.mock.MagicMock(side_effect=services.NotMine('foo'))
        with self.assertRaises(services.NotMine):
            services.NoteService.create_new({'key': 'value'})

    @base.TestCase.mock.patch('app.house.wall.Note.list_for_user')
    def test_list(self, list_mock):
        services.NoteService.list_for_user(1)
        self.assertTrue(list_mock.called)

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_delete(self, note_mock):
        note_instance_mock = self.mock.MagicMock()
        note_mock.create_for_user.return_value = note_instance_mock
        note_instance_mock.delete.return_value = None
        services.NoteService.delete(1, 1)
        self.assertTrue(note_instance_mock.delete_db.called)

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_update_by_id(self, note_mock):
        note_instance_mock = self.mock.MagicMock()
        note_mock.create_for_user.return_value = note_instance_mock
        note_instance_mock.update.return_value = None
        services.NoteService.update_by_id(1, {'i am': 'a python dict'}, 1)
        self.assertTrue(note_instance_mock.update.called)
