from tests import base


class ScribeFactoryCreateWithEnvironmentTest(base.TestCase):

    def test_should_call_local_scribe_to_create_with_router_for_user_if_config_is_development(self):
        pass

    def test_should_call_s3_scribe_to_create_with_router_for_user_if_config_is_production(self):
        pass

    def test_should_raise_invalid_env_if_config_nether_development_or_production(self):
        pass


class AvatarScribeSaveTest(base.TestCase):

    def test_should_raise_not_implemented(self):
        pass


class AvatarScribeUserIdTest(base.TestCase):

    def test_has_user_id(self):
        pass


class AvatarScribeRouterTest(base.TestCase):

    def test_has_router(self):
        pass


class LocalScribeSaveTest(base.TestCase):

    def test_should_call_os_to_check_if_path_exists(self):
        pass

    def test_should_call_os_to_makedirs_if_path_dont_exists(self):
        pass

    def test_should_call_shutil_to_move_file_to_router_path(self):
        pass

    def test_should_return_router_file_path(self):
        pass


class LocalScribeCreateWithRouterForUserTest(base.TestCase):

    def test_should_raise_invalid_router_if_router_is_not_avatar(self):
        pass

    def test_should_call_avatar_directory_router_to_create_for_user(self):
        pass

    def test_should_return_instance(self):
        pass


class S3ScribeCreateWithRouterForUserTest(base.TestCase):

    def test_should_get_S3_AWS_ACCESS_KEY_ID_with_config(self):
        pass

    def test_should_get_S3_AWS_SECRET_ACCESS_KEY_with_config(self):
        pass

    def test_should_get_S3_AWS_BUCKET_NAME_with_config(self):
        pass

    def test_should_get_call_boto3_to_instantiate_client(self):
        pass

    def test_should_raise_invalid_router_if_router_is_not_avatar(self):
        pass

    def test_should_call_avatar_directory_router_to_create_for_user(self):
        pass

    def test_should_return_instance(self):
        pass


class S3ScribeSave(base.TestCase):

    def test_should_call_s3_client_to_upload_file(self):
        pass

    def test_should_return_router_file_name(self):
        pass
