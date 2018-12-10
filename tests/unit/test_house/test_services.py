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


class FileServiceSaveAvatarTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.services.drawer.File')
    def test_should_call_drawer_file_to_create_with_environment(self, file_mock):
        file_instance = self.mock.MagicMock()
        file_mock.create_with_environment.return_value = file_instance
        services.FileService.save_avatar('/some_path', 1)
        file_mock.create_with_environment.assert_called_with(1, router='avatar')

    @base.TestCase.mock.patch('app.house.services.drawer.File')
    def test_should_call_drawer_file_to_save(self, file_mock):
        file_instance = self.mock.MagicMock()
        file_mock.create_with_environment.return_value = file_instance
        file_instance.save.return_value = '/path'
        services.FileService.save_avatar('/some_path', 1)
        file_instance.save.assert_called_with('/some_path')

    @base.TestCase.mock.patch('app.house.services.drawer.File')
    def test_should_return_file_path(self, file_mock):
        file_instance = self.mock.MagicMock()
        file_mock.create_with_environment.return_value = file_instance
        file_instance.save.return_value = '/path'
        path = services.FileService.save_avatar('/some_path', 1)
        self.assertEqual('/path', path)


class SecurityServiceGenerateTokenTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.services.secrets.token_hex')
    def test_should_call_secrets_to_token_hex(self, token_hex_mock):
        token_hex_mock.return_value = 'testyjednostkowe'
        services.SecurityService.generate_a_token()
        token_hex_mock.assert_called_with(40)

    @base.TestCase.mock.patch('app.house.services.secrets.token_hex')
    def test_should_return_token(self, token_hex_mock):
        token_hex_mock.return_value = 'testyjednostkowe'
        token = services.SecurityService.generate_a_token()
        self.assertEqual(token, 'testyjednostkowe')


class SecurityServiceHashTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.services.pbkdf2_sha256.hash')
    def test_should_call_pbfkd2_sha256_to_hash(self, hash_mock):
        hash_mock.return_value = 'testyjednostkowe'
        services.SecurityService.hash('slowo')
        hash_mock.assert_called_with('slowo')

    @base.TestCase.mock.patch('app.house.services.pbkdf2_sha256.hash')
    def test_should_return_hash(self, hash_mock):
        hash_mock.return_value = 'testyjednostkowe'
        haash = services.SecurityService.hash('slowo')
        self.assertEqual(haash, 'testyjednostkowe')


class SecurityServiceIsStringEqualsToHashTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.services.pbkdf2_sha256.verify')
    def test_should_call_pbfkd2_sha256_to_verify(self, verify_mock):
        verify_mock.return_value = True
        services.SecurityService.is_string_equals_to_hash('slowo', 'testyjednostkowe')
        verify_mock.assert_called_with('slowo', 'testyjednostkowe')

    @base.TestCase.mock.patch('app.house.services.pbkdf2_sha256.verify')
    def test_should_return_true_if_string_is_equals_to_hash(self, verify_mock):
        verify_mock.return_value = True
        is_equal = services.SecurityService.is_string_equals_to_hash('slowo', 'testyjednostkowe')
        self.assertTrue(is_equal)

    @base.TestCase.mock.patch('app.house.services.pbkdf2_sha256.verify')
    def test_should_return_false_if_string_is_not_equals_to_hash(self, verify_mock):
        verify_mock.return_value = False
        is_equal = services.SecurityService.is_string_equals_to_hash('slowo', 'testyjednostkowe')
        self.assertFalse(is_equal)
