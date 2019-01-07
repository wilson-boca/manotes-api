from tests import base
from app import exceptions
from app.house import residents


class UserCreateWithIdTest(base.TestCase):
    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_should_return_instance(self, repository_mock):
        user_mocked = self.mock.MagicMock('something')
        user_mocked.id = 1
        repository_mock.one_or_none.return_value = user_mocked
        user_created = residents.User.create_with_id(1)
        self.assertTrue(isinstance(user_created, residents.User))

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_should_raise_not_found_if_id_dont_exists(self, repository_mock):
        repository_mock.one_or_none.return_value = None
        with self.assertRaises(exceptions.NotFound):
            residents.User.create_with_id(1)


class UserCreateWithInstanceTest(base.TestCase):
    def test_create_with_instance_should_return_instance(self):
        instance_mocked = self.mock.MagicMock('something')
        instance_mocked.id = 1
        user_created = residents.User.create_with_instance(instance_mocked)
        self.assertTrue(isinstance(user_created, residents.User))


class UserCreateWithToken(base.TestCase):
    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_should_return_instance(self, repository_mock):
        user_mocked = self.mock.MagicMock('something')
        user_mocked.id = 1
        repository_mock.one_or_none.return_value = user_mocked
        user_created = residents.User.create_with_token('UsErRToKeN')
        self.assertTrue(isinstance(user_created, residents.User))

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_should_raise_not_found_if_token_dont_exists(self, repository_mock):
        repository_mock.one_or_none.return_value = None
        with self.assertRaises(exceptions.NotFound):
            residents.User.create_with_token('UsErRToKeN')


class UserNotesTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_should_call_service_if_not_cached(self, note_service):
        note_service.list_for_user.return_value = []
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        notes = user.notes
        self.assertTrue(note_service.list_for_user.called)
        self.assertEqual(notes, [])

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_should_return_notes_if_cached(self, note_service):
        note_service.list_for_user.return_value = []
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        user._notes = []
        notes = user.notes
        self.assertFalse(note_service.list_for_user.called)
        self.assertEqual(notes, [])


class UserCreateWithUsernameTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_should_return_instance(self, repository_mock):
        user_mocked = self.mock.MagicMock('something')
        user_mocked.id = 1
        repository_mock.one_or_none.return_value = user_mocked
        user_created = residents.User.create_with_username('breno')
        self.assertTrue(isinstance(user_created, residents.User))

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_should_raise_not_found_if_username_dont_exists(self, repository_mock):
        repository_mock.one_or_none.return_value = None
        with self.assertRaises(exceptions.NotFound):
            residents.User.create_with_username('UsErRToKeN')


class UserCreateWithEmailTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_should_return_instance(self, repository_mock):
        user_mocked = self.mock.MagicMock('something')
        user_mocked.id = 1
        repository_mock.one_or_none.return_value = user_mocked
        user_created = residents.User.create_with_email('breno')
        self.assertTrue(isinstance(user_created, residents.User))

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_should_raise_not_found_if_username_dont_exists(self, repository_mock):
        repository_mock.one_or_none.return_value = None
        with self.assertRaises(exceptions.NotFound):
            residents.User.create_with_email('UsErRToKeN')


class UserGetANoteTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_should_call_services_to_instantiate(self, note_service_mock):
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        user.get_a_note(1)
        self.assertTrue(note_service_mock.create_for_user.called)


class UserCreateANoteTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_should_call_services_to_create_new(self, note_service_mock):
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        note = {
            'id': '1',
            'name': 'this is a note',
            'content': 'This is a note',
            'color': '#FFFFFF'
        }
        user = residents.User(db_instance=db_instance)
        user.create_a_note(note)
        self.assertTrue(note_service_mock.create_new.called)


class UpdateANoteTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_should_call_services_to_instantiate(self, note_service_note):
        note_mock = self.mock.MagicMock()
        note_service_note.create_for_user.return_value = note_mock
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        note_changes = {
            'id': '1',
            'name': 'this is a note',
            'content': 'This is a note',
            'color': '#FFFFFF'
        }
        user.update_a_note(id=1, note_changes=note_changes)
        self.assertTrue(note_service_note.create_for_user.called)

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_should_call_update_if_note_was_instantiated(self, note_service_note):
        note_mock = self.mock.MagicMock()
        note_service_note.create_for_user.return_value = note_mock
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        note_changes = {
            'id': '1',
            'name': 'this is a note',
            'content': 'This is a note',
            'color': '#FFFFFF'
        }
        user.update_a_note(id=1, note_changes=note_changes)
        self.assertTrue(note_mock.update.called)


class UserDeleteANoteTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_should_call_services_to_instantiate(self, note_service_note):
        note_mock = self.mock.MagicMock()
        note_service_note.create_for_user.return_value = note_mock
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        user.delete_a_note(id=1)
        self.assertTrue(note_service_note.create_for_user)

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_should_call_delete_if_note_instantiated(self, note_service_note):
        note_mock = self.mock.MagicMock()
        note_service_note.create_for_user.return_value = note_mock
        db_instance = self.mock.MagicMock()
        db_instance.id = 1
        user = residents.User(db_instance=db_instance)
        user.delete_a_note(id=1)
        self.assertTrue(note_mock.delete.called)
