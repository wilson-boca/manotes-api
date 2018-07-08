from tests import base
from app.house import residents, services


class UserTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_notes_call_service_if_not_cached(self, note_service):
        note_service.list_for_user.return_value = []
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        notes = user.notes
        self.assertTrue(note_service.list_for_user.called)
        self.assertEqual(notes, [])

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_notes_return_notes_if_cached(self, note_service):
        note_service.list_for_user.return_value = []
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        user._notes = []
        notes = user.notes
        self.assertFalse(note_service.list_for_user.called)
        self.assertEqual(notes, [])

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_create_with_id(self, repository_mock):
        user_mocked = self.mock.MagicMock('something')
        user_mocked.id = 1
        repository_mock.one_or_none.return_value = user_mocked
        user_created = residents.User.create_with_id(1)
        self.assertTrue(isinstance(user_created, residents.User))

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_create_with_id_raise_not_found(self, repository_mock):
        repository_mock.one_or_none.return_value = None
        with self.assertRaises(residents.NotFound):
            residents.User.create_with_id(1)

    def test_create_with_instance(self):
        instance_mocked = self.mock.MagicMock('something')
        instance_mocked.id = 1
        user_created = residents.User.create_with_instance(instance_mocked)
        self.assertTrue(isinstance(user_created, residents.User))

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_create_with_token(self, repository_mock):
        user_mocked = self.mock.MagicMock('something')
        user_mocked.id = 1
        repository_mock.one_or_none.return_value = user_mocked
        user_created = residents.User.create_with_token('UsErRToKeN')
        self.assertTrue(isinstance(user_created, residents.User))

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_create_with_token_raise_not_found(self, repository_mock):
        repository_mock.one_or_none.return_value = None
        with self.assertRaises(residents.NotFound):
            residents.User.create_with_token('UsErRToKeN')

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_create_with_username(self, repository_mock):
        user_mocked = self.mock.MagicMock('something')
        user_mocked.id = 1
        repository_mock.one_or_none.return_value = user_mocked
        user_created = residents.User.create_with_username('breno')
        self.assertTrue(isinstance(user_created, residents.User))

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_create_with_username_raise_not_found(self, repository_mock):
        repository_mock.one_or_none.return_value = None
        with self.assertRaises(residents.NotFound):
            residents.User.create_with_username('UsErRToKeN')

    @base.TestCase.mock.patch('app.house.services.NoteService.create_for_user')
    def test_get_a_note(self, create_for_user_mock):
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        user.get_a_note(1)
        self.assertTrue(create_for_user_mock.called)

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_get_a_note_return_not_found(self, note_service_mock):
        note_service_mock.create_for_user = self.mock.MagicMock(side_effect=services.NotFound('foo'))
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        with self.assertRaises(residents.NotFound):
            user.get_a_note(1)

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_get_a_note_return_not_mine(self, note_service_mock):
        note_service_mock.create_for_user = self.mock.MagicMock(side_effect=services.NotMine('foo'))
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        with self.assertRaises(residents.NotMine):
            user.get_a_note(1)

    @base.TestCase.mock.patch('app.house.services.NoteService.create_new')
    def test_create_a_note(self, create_new_mock):
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        note_json = {
            'id': '1',
            'name': 'this is a note',
            'content': 'This is a note',
            'color': '#FFFFFF'
        }
        user = residents.User(db_instance=db_instance)
        user.create_a_note(note_json)
        self.assertTrue(create_new_mock.called)

    @base.TestCase.mock.patch('app.house.services.NoteService.update_by_id')
    def test_update_a_note(self, update_mock):
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        note_json = {
            'id': '1',
            'name': 'this is a note',
            'content': 'This is a note',
            'color': '#FFFFFF'
        }
        user.update_a_note(id=1, note_json=note_json)
        self.assertTrue(update_mock.called)

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_update_a_note_raise_not_found(self, note_service):
        note_service.update_by_id = self.mock.MagicMock(side_effect=services.NotFound('foo'))
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        note_json = {
            'id': '1',
            'name': 'this is a note',
            'content': 'This is a note',
            'color': '#FFFFFF'
        }
        with self.assertRaises(residents.NotFound):
            user.update_a_note(id=1, note_json=note_json)

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_update_a_note_raise_not_mine(self, note_service):
        note_service.update_by_id = self.mock.MagicMock(side_effect=services.NotMine('foo'))
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        note_json = {
            'id': '1',
            'name': 'this is a note',
            'content': 'This is a note',
            'color': '#FFFFFF'
        }
        with self.assertRaises(residents.NotMine):
            user.update_a_note(id=1, note_json=note_json)

    @base.TestCase.mock.patch('app.house.services.NoteService.delete')
    def test_delete_a_note(self, delete_a_note):
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        user.delete_a_note(id=1)
        self.assertTrue(delete_a_note.called)

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_delete_a_note_raise_not_found(self, note_service):
        note_service.delete = self.mock.MagicMock(side_effect=services.NotFound('foo'))
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        with self.assertRaises(residents.NotFound):
            user.delete_a_note(id=1)

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_delete_a_note_raise_not_mine(self, note_service):
        note_service.delete = self.mock.MagicMock(side_effect=services.NotMine('foo'))
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        with self.assertRaises(residents.NotMine):
            user.delete_a_note(id=1)
