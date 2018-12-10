from tests import base
from app import exceptions
from app.house import residents, services


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
        note_json = {
            'id': '1',
            'name': 'this is a note',
            'content': 'This is a note',
            'color': '#FFFFFF'
        }
        user = residents.User(db_instance=db_instance)
        user.create_a_note(note_json)
        self.assertTrue(note_service_mock.create_new.called)


class UpdateANoteTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_should_call_services_to_instantiate(self, note_service_note):
        note_mock = self.mock.MagicMock()
        note_service_note.create_for_user.return_value = note_mock
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
        self.assertTrue(note_service_note.create_for_user.called)

    @base.TestCase.mock.patch('app.house.services.NoteService')
    def test_should_call_update_if_note_was_instantiated(self, note_service_note):
        note_mock = self.mock.MagicMock()
        note_service_note.create_for_user.return_value = note_mock
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


class VisitorUserCreateAccountTest(base.TestCase):

    @base.TestCase.mock.patch('app.async_tasks.tasks.start_send_email')
    @base.TestCase.mock.patch('app.house.services.SecurityService')
    @base.TestCase.mock.patch('app.house.residents.VisitorUser.repository')
    def test_should_call_security_service_to_hash_password(self, repository_mock, security_service_mock, start_send_email_mock):
        db_instance_mock = self.mock.MagicMock()
        security_service_mock.generate_a_token.return_value = 'qwertyasdfgzxcvb'
        security_service_mock.hash.return_value = 'qwr324!&8@@333'
        start_send_email_mock.start_send_email.return_value = 10
        repository_mock.create_from_json.return_value = db_instance_mock
        payload = {'username': 'breno', 'password': 12345}
        residents.VisitorUser.create_account(payload)
        self.assertTrue(security_service_mock.hash.called)

    @base.TestCase.mock.patch('app.async_tasks.tasks.start_send_email')
    @base.TestCase.mock.patch('app.house.services.SecurityService')
    @base.TestCase.mock.patch('app.house.residents.VisitorUser.repository')
    def test_should_call_security_service_to_generate_token(self, repository_mock, security_service_mock, start_send_email_mock):
        db_instance_mock = self.mock.MagicMock()
        security_service_mock.generate_a_token.return_value = 'qwertyasdfgzxcvb'
        security_service_mock.hash.return_value = 'qwr324!&8@@333'
        start_send_email_mock.start_send_email.return_value = 10
        repository_mock.create_from_json.return_value = db_instance_mock
        payload = {'username': 'breno', 'password': 12345}
        residents.VisitorUser.create_account(payload)
        self.assertTrue(security_service_mock.generate_a_token.called)

    @base.TestCase.mock.patch('app.async_tasks.tasks.start_send_email')
    @base.TestCase.mock.patch('app.house.services.SecurityService')
    @base.TestCase.mock.patch('app.house.residents.VisitorUser.repository')
    def test_should_call_repository_to_create_from_json(self, repository_mock, security_service_mock, start_send_email_mock):
        db_instance_mock = self.mock.MagicMock()
        security_service_mock.generate_a_token.return_value = 'qwertyasdfgzxcvb'
        security_service_mock.hash.return_value = 'qwr324!&8@@333'
        start_send_email_mock.return_value = 10
        repository_mock.create_from_json.return_value = db_instance_mock
        payload = {'username': 'breno', 'password': 12345}
        residents.VisitorUser.create_account(payload)
        self.assertTrue(repository_mock.create_from_json.called)

    @base.TestCase.mock.patch('app.async_tasks.tasks.start_send_email')
    @base.TestCase.mock.patch('app.house.services.SecurityService')
    @base.TestCase.mock.patch('app.house.residents.VisitorUser.repository')
    def test_should_call_tasks_to_start_send_email(self, repository_mock, security_service_mock, start_send_email_mock):
        db_instance_mock = self.mock.MagicMock()
        security_service_mock.generate_a_token.return_value = 'qwertyasdfgzxcvb'
        security_service_mock.hash.return_value = 'qwr324!&8@@333'
        start_send_email_mock.start_send_email.return_value = 10
        repository_mock.create_from_json.return_value = db_instance_mock
        payload = {'username': 'breno', 'password': 12345}
        residents.VisitorUser.create_account(payload)
        self.assertTrue(repository_mock.create_from_json.called)

    @base.TestCase.mock.patch('app.async_tasks.tasks.start_send_email')
    @base.TestCase.mock.patch('app.house.services.SecurityService')
    @base.TestCase.mock.patch('app.house.residents.VisitorUser.repository')
    def test_should_return_user_instance(self, repository_mock, security_service_mock, start_send_email_mock):
        db_instance_mock = self.mock.MagicMock()
        security_service_mock.generate_a_token.return_value = 'qwertyasdfgzxcvb'
        security_service_mock.hash.return_value = 'qwr324!&8@@333'
        start_send_email_mock.start_send_email.return_value = 10
        repository_mock.create_from_json.return_value = db_instance_mock
        payload = {'username': 'breno', 'password': 12345}
        user = residents.VisitorUser.create_account(payload)
        self.assertTrue(isinstance(user, residents.User))
