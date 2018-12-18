from tests import base


class ConfigTest(base.TestCase):

    def test_has_DEBUG_default_false(self):
        pass

    def test_has_TESTING_default_false(self):
        pass

    def test_has_DEVELOPMENT_default_false(self):
        pass

    def test_has_ENVIRONMENT_default_development(self):
        pass

    def test_has_SQLALCHEMY_DATABASE_URI_from_environment(self):
        pass

    def test_has_REDIS_from_environment(self):
        pass

    def test_has_SMTP_HOST_from_environment(self):
        pass

    def test_has_SMTP_PORT_from_environment(self):
        pass

    def test_has_SMTP_USERNAME_from_environment(self):
        pass

    def test_has_SMTP_PASSWORD_from_environment(self):
        pass

    def test_has_FILE_STORAGE_PATH_from_environment(self):
        pass

    def test_has_AVATAR_BUCKET_NAME_from_environment(self):
        pass

    def test_has_S3_AWS_ACCESS_KEY_ID_from_environmnet(self):
        pass

    def test_has_S3_AWS_SECRET_ACCESS_KEY_from_environment(self):
        pass

    def test_has_TEMP_PATH_from_environment(self):
        pass


class ProductionConfigTest(base.TestCase):

    def test_has_PRODUCTION_default_true(self):
        pass


class DevelopmentConfigTest(base.TestCase):

    def test_has_DEBUG_default_true(self):
        pass

    def test_has_DEVELOPMENT_default_true(self):
        pass

    def test_has_SQLALCHEMY_RECORD_QUERIES_default_true(self):
        pass


class TestingConfigTest(base.TestCase):

    def test_has_TESTING_default_true(self):
        pass

    def test_has_KEY_ON_TEST_default_KEY_ON_TEST(self):
        pass

    def test_has_ENVIRONMENT_default_test(self):
        pass


class GetConfigTest(base.TestCase):

    def test_should_call_os_environ_to_APP_SETTINGS(self):
        pass

    def test_should_call_import_module_to_import_config_module(self):
        pass

    def test_should_raise_config_class_not_found_if_config_class_is_none(self):
        pass

    def test_should_return_config_class_if_config_class(self):
        pass
