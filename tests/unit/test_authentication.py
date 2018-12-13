from tests import base
from app import authentication


class AuthServiceAuthenticateWithCredentials(base.TestCase):

    def test_should_call_create_with_username(self):
        pass

    def test_should_raise_user_not_exists_if_not_found_raised(self):
        pass

    def test_should_call_security_service_to_is_strong_equals_to_hash(self):
        pass

    def test_should_return_authenticated(self):
        pass

    def test_should_return_user_instance(self):
        pass


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
