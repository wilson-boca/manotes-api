from tests import base
from app.house import services


class NoteServiceCreateNewTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_create_new_should_call_entity_to_create_new(self, note_mock):
        note_mock.create_new = self.mock.MagicMock(return_value=None)
        services.NoteService.create_new({'key': 'value'})
        self.assertTrue(note_mock.create_new.called)

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_create_new_should_return_new_instance_created(self, note_mock):
        new_note_mock = self.mock.MagicMock()
        note_mock.create_new = self.mock.MagicMock(return_value=new_note_mock)
        new_note = services.NoteService.create_new({'key': 'value'})
        self.assertEqual(new_note_mock, new_note)


class NoteServiceListForUserTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_list_for_user_should_call_entity_to_list(self, note_mock):
        note_mock.list_for_user = self.mock.MagicMock(return_value=None)
        services.NoteService.list_for_user(1)
        self.assertTrue(note_mock.list_for_user.called)

    @base.TestCase.mock.patch('app.house.wall.Note')
    def test_list_for_user_should_return_list(self, note_mock):
        note_mock.list_for_user = self.mock.MagicMock(return_value=[])
        notes = services.NoteService.list_for_user(1)
        self.assertTrue(isinstance(notes, list))
