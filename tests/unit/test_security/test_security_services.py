from tests import base
from app.security import security_services


class TokenServiceGenerateTokenTest(base.TestCase):

    @base.TestCase.mock.patch('app.security.security_services.secrets.token_hex')
    def test_should_call_secrets_to_token_hex(self, token_hex_mock):
        token_hex_mock.return_value = 'testyjednostkowe'
        security_services.TokenService.generate()
        token_hex_mock.assert_called_with(40)

    @base.TestCase.mock.patch('app.security.security_services.secrets.token_hex')
    def test_should_return_token(self, token_hex_mock):
        token_hex_mock.return_value = 'testyjednostkowe'
        token = security_services.TokenService.generate()
        self.assertEqual(token, 'testyjednostkowe')


class HashServiceHashTest(base.TestCase):

    @base.TestCase.mock.patch('app.security.security_services.pbkdf2_sha256.hash')
    def test_should_call_pbfkd2_sha256_to_hash(self, hash_mock):
        hash_mock.return_value = 'testyjednostkowe'
        security_services.HashService.hash('slowo')
        hash_mock.assert_called_with('slowo')

    @base.TestCase.mock.patch('app.security.security_services.pbkdf2_sha256.hash')
    def test_should_return_hash(self, hash_mock):
        hash_mock.return_value = 'testyjednostkowe'
        haash = security_services.HashService.hash('slowo')
        self.assertEqual(haash, 'testyjednostkowe')


class SecurityServiceIsStringEqualsToHashTest(base.TestCase):

    @base.TestCase.mock.patch('app.security.security_services.pbkdf2_sha256.verify')
    def test_should_call_pbfkd2_sha256_to_verify(self, verify_mock):
        verify_mock.return_value = True
        security_services.HashService.is_string_equals_to_hash('slowo', 'testyjednostkowe')
        verify_mock.assert_called_with('slowo', 'testyjednostkowe')

    @base.TestCase.mock.patch('app.security.security_services.pbkdf2_sha256.verify')
    def test_should_return_true_if_string_is_equals_to_hash(self, verify_mock):
        verify_mock.return_value = True
        is_equal = security_services.HashService.is_string_equals_to_hash('slowo', 'testyjednostkowe')
        self.assertTrue(is_equal)

    @base.TestCase.mock.patch('app.security.security_services.pbkdf2_sha256.verify')
    def test_should_return_false_if_string_is_not_equals_to_hash(self, verify_mock):
        verify_mock.return_value = False
        is_equal = security_services.HashService.is_string_equals_to_hash('slowo', 'testyjednostkowe')
        self.assertFalse(is_equal)
