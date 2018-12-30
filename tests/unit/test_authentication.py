from tests import base
from app import authentication, exceptions


class AuthServiceAuthenticateWithCredentials(base.TestCase):

    @base.mock.patch('app.house.services.SecurityService.is_string_equals_to_hash', base.mock.MagicMock())
    @base.mock.patch('app.house.residents.User.create_with_username')
    def test_should_call_create_with_username(self, create_with_username_mock):
        authentication.AuthService.authenticate_with_credentials({'username': 'breno', 'password': 12345})
        create_with_username_mock.assert_called_with('breno')

    @base.mock.patch('app.house.services.SecurityService.is_string_equals_to_hash', base.mock.MagicMock())
    @base.mock.patch('app.house.residents.User.create_with_username', base.mock.MagicMock(side_effect=exceptions.NotFound))
    def test_should_raise_user_not_exists_if_not_found_raised(self):
        with self.assertRaises(exceptions.UserNotExists):
            authentication.AuthService.authenticate_with_credentials({'username': 'breno', 'password': 12345})

    @base.mock.patch('app.house.services.SecurityService.is_string_equals_to_hash')
    @base.mock.patch('app.house.residents.User.create_with_username')
    def test_should_call_security_service_to_is_strong_equals_to_hash(self, create_with_username_mock, is_string_equals_to_hash_mock):
        user_mock = self.mock.MagicMock()
        user_mock.password = 'fjsadufhnejbadf'
        create_with_username_mock.return_value = user_mock
        authentication.AuthService.authenticate_with_credentials({'username': 'breno', 'password': 12345})
        is_string_equals_to_hash_mock.assert_called_with(12345, 'fjsadufhnejbadf')

    @base.mock.patch('app.house.services.SecurityService.is_string_equals_to_hash')
    @base.mock.patch('app.house.residents.User.create_with_username')
    def test_should_return_authenticated(self, create_with_username_mock, is_string_equals_to_hash):
        is_string_equals_to_hash.return_value = True
        user_mock = self.mock.MagicMock()
        user_mock.password = 'FHSDAUHENKGA'
        create_with_username_mock.return_value = user_mock
        authenticated, user = authentication.AuthService.authenticate_with_credentials({'username': 'breno', 'password': 12345})
        self.assertTrue(authenticated)

    @base.mock.patch('app.house.services.SecurityService.is_string_equals_to_hash')
    @base.mock.patch('app.house.residents.User.create_with_username')
    def test_should_return_user_instance(self, create_with_username_mock, is_string_equals_to_hash):
        is_string_equals_to_hash.return_value = True
        user_mock = self.mock.MagicMock()
        user_mock.password = 'FHSDAUHENKGA'
        create_with_username_mock.return_value = user_mock
        authenticated, user = authentication.AuthService.authenticate_with_credentials({'username': 'breno', 'password': 12345})
        self.assertEqual(user, user_mock)


class AuthServiceAuthenticateWithToken(base.TestCase):

    def test_should_call_create_with_token(self):
        pass

    def test_should_set_user_on_g_if_not_found_not_raised(self):
        pass

    def test_should_set_current_token_on_if_not_found_not_raised(self):
        pass

    def test_should_set_authenticated_true_on_g_if_not_found_not_raised(self):
        pass

    def test_should_set_authenticated_false_on_g_if_not_found_raised(self):
        pass
