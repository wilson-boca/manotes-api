from app.store import reception
from tests import base


class ClerkCreateAccountTest(base.TestCase):

    @base.TestCase.mock.patch('app.async_tasks.tasks.start_send_email')
    @base.TestCase.mock.patch('app.security.security_services.TokenService')
    @base.TestCase.mock.patch('app.security.security_services.HashService')
    @base.TestCase.mock.patch('app.house.services.UserService')
    def test_should_call_hash_service_to_hash_password(self, user_service_mock, hash_service_mock, token_service_mock, start_send_email_mock):
        user_mock = self.mock.MagicMock()
        token_service_mock.generate.return_value = 'qwertyasdfgzxcvb'
        hash_service_mock.hash.return_value = 'qwr324!&8@@333'
        start_send_email_mock.start_send_email.return_value = 10
        user_service_mock.create_new.return_value = user_mock
        payload = {'username': 'breno', 'password': 12345}
        reception.Clerk.create_user_account(payload)
        self.assertTrue(hash_service_mock.hash.called)

    @base.TestCase.mock.patch('app.security.security_services.HashService', base.mock.MagicMock())
    @base.TestCase.mock.patch('app.async_tasks.tasks.start_send_email')
    @base.TestCase.mock.patch('app.security.security_services.TokenService')
    @base.TestCase.mock.patch('app.house.services.UserService')
    def test_should_call_token_service_to_generate(self, user_service_mock, token_service_mock, start_send_email_mock):
        user_mock = self.mock.MagicMock()
        token_service_mock.generate_a_token.return_value = 'qwertyasdfgzxcvb'
        token_service_mock.hash.return_value = 'qwr324!&8@@333'
        start_send_email_mock.start_send_email.return_value = 10
        user_service_mock.create_new.return_value = user_mock
        payload = {'username': 'breno', 'password': 12345}
        reception.Clerk.create_user_account(payload)
        self.assertTrue(token_service_mock.generate.called)

    @base.TestCase.mock.patch('app.async_tasks.tasks.start_send_email')
    @base.TestCase.mock.patch('app.security.security_services.TokenService')
    @base.TestCase.mock.patch('app.security.security_services.HashService')
    @base.TestCase.mock.patch('app.house.services.UserService')
    def test_should_user_service_to_create_new(self, user_service_mock, hash_service_mock, token_service_mock, start_send_email_mock):
        user_mock = self.mock.MagicMock()
        token_service_mock.generate_a_token.return_value = 'qwertyasdfgzxcvb'
        hash_service_mock.hash.return_value = 'qwr324!&8@@333'
        start_send_email_mock.return_value = 10
        user_service_mock.create_new.return_value = user_mock
        payload = {'username': 'breno', 'password': 12345}
        reception.Clerk.create_user_account(payload)
        self.assertTrue(user_service_mock.create_new.called)

    @base.TestCase.mock.patch('app.async_tasks.tasks.start_send_email')
    @base.TestCase.mock.patch('app.security.security_services.TokenService')
    @base.TestCase.mock.patch('app.security.security_services.HashService')
    @base.TestCase.mock.patch('app.house.services.UserService')
    def test_should_call_tasks_to_start_send_email(self, user_service_mock, hash_service_mock, token_service_mock, start_send_email_mock):
        user_mock = self.mock.MagicMock()
        token_service_mock.generate.return_value = 'qwertyasdfgzxcvb'
        hash_service_mock.hash.return_value = 'qwr324!&8@@333'
        start_send_email_mock.start_send_email.return_value = 10
        user_service_mock.create_from_dict.return_value = user_mock
        payload = {'username': 'breno', 'password': 12345}
        reception.Clerk.create_user_account(payload)
        self.assertTrue(start_send_email_mock.called)

    @base.TestCase.mock.patch('app.async_tasks.tasks.start_send_email')
    @base.TestCase.mock.patch('app.security.security_services.TokenService')
    @base.TestCase.mock.patch('app.security.security_services.HashService')
    @base.TestCase.mock.patch('app.house.services.UserService')
    def test_should_return_user_instance(self, user_service_mock, hash_service_mock, token_service_mock, start_send_email_mock):
        user_mock = self.mock.MagicMock()
        token_service_mock.generate.return_value = 'qwertyasdfgzxcvb'
        hash_service_mock.hash.return_value = 'qwr324!&8@@333'
        start_send_email_mock.start_send_email.return_value = 10
        user_service_mock.create_new.return_value = user_mock
        payload = {'username': 'breno', 'password': 12345}
        created_user = reception.Clerk.create_user_account(payload)
        self.assertEqual(created_user, user_mock)
