from tests import base


class BeforeRequestTest(base.TestCase):

    @base.mock.MagicMock('app.authentication.AuthService.authenticate_with_token')
    @base.mock.MagicMock('app.initialize.request.cookies')
    def test_should_call_cookies_to_get_user_token(self, cookies_mock, authenticate_with_token_mock):
        base.initialize.before_request()
        self.assertTrue(cookies_mock.called)

    @base.mock.MagicMock('app.authentication.AuthService.authenticate_with_token')
    @base.mock.MagicMock('app.initialize.request.cookies')
    def test_should_call_auth_service_to_authenticate_with_token(self, cookies_mock, authenticate_with_token_mock):
        base.initialize.before_request()
        self.assertTrue(authenticate_with_token_mock.called)


class AddTokenHeaderTest(base.TestCase):

    def test_should_call_g_to_get_user(self):
        pass

    def test_g_has_current_token_if_user_is_not_none(self):
        pass

    def test_should_call_datetime_to_get_time_now(self):
        pass

    def test_should_call_datetime_to_timedelta_with_90_days(self):
        pass

    def test_has_expire_date_with_last_90_days(self):
        pass

    def test_should_call_response_to_set_user_token(self):
        pass


class CreateApiTest(base.TestCase):

    def test_should_call_web_app_to_run(self):
        pass

    def test_should_call_config_to_get_port(self):
        pass


class RunTest(base.TestCase):

    def test_should_call_create_api(self):
        pass

    def test_should_call_web_app_to_run(self):
        pass
