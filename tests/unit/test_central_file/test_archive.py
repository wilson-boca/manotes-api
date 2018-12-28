from tests import base
from app import exceptions
from app.central_files import archive


class ScribeFactoryCreateWithEnvironmentTest(base.TestCase):

    @base.mock.patch('app.central_files.archive.LocalScribe')
    @base.mock.patch('app.central_files.archive.config')
    def test_should_call_local_scribe_to_create_with_router_for_user_if_config_is_development(self, config_mock, local_scribe_mock):
        config_mock.PRODUCTION = None
        config_mock.DEVELOPMENT.return_value = self.mock.MagicMock()
        archive.ScribeFactory.create_with_environment(1, self.mock.MagicMock())
        self.assertTrue(local_scribe_mock.create_with_router_for_user.called)

    @base.mock.patch('app.central_files.archive.S3Scribe')
    @base.mock.patch('app.central_files.archive.config')
    def test_should_call_s3_scribe_to_create_with_router_for_user_if_config_is_production(self, config_mock, s3_scribe_mock):
        config_mock.DEVELOPMENT = None
        config_mock.PRODUCTION.return_value = self.mock.MagicMock()
        archive.ScribeFactory.create_with_environment(1, self.mock.MagicMock())
        self.assertTrue(s3_scribe_mock.create_with_router_for_user.called)

    @base.mock.patch('app.central_files.archive.config')
    def test_should_raise_invalid_env_if_config_nether_development_or_production(self, config_mock):
        config_mock.DEVELOPMENT = None
        config_mock.PRODUCTION = None
        with self.assertRaises(exceptions.InvalidEnvironment):
            archive.ScribeFactory.create_with_environment(1, self.mock.MagicMock())


class AvatarScribeSaveTest(base.TestCase):

    def test_should_raise_not_implemented(self):
        abstract_scribe = archive.AbstractScribe(1, self.mock.MagicMock())
        with self.assertRaises(exceptions.NoImplementationError):
            abstract_scribe.save(file=self.mock.MagicMock())


class AvatarScribeUserIdTest(base.TestCase):

    def test_has_user_id(self):
        abstract_scribe = archive.AbstractScribe(1, self.mock.MagicMock())
        self.assertEqual(1, abstract_scribe.user_id)


class AvatarScribeRouterTest(base.TestCase):

    def test_has_router(self):
        router_mock = self.mock.MagicMock()
        abstract_scribe = archive.AbstractScribe(1, router_mock)
        self.assertEqual(router_mock, abstract_scribe.router)


class LocalScribeCreateWithRouterForUserTest(base.TestCase):

    def test_should_raise_invalid_router_if_router_is_not_avatar(self):
        with self.assertRaises(exceptions.InvalidRouter):
            archive.LocalScribe.create_with_router_for_user(1, 'asdf')

    @base.mock.patch('app.central_files.archive.AvatarDirectoryRouter.create_for_user')
    def test_should_call_avatar_directory_router_to_create_for_user_if_router_is_avatar(self, create_for_user_mock):
        archive.LocalScribe.create_with_router_for_user(1, 'avatar')
        self.assertTrue(create_for_user_mock.called)

    def test_should_return_instance(self):
        local_scribe_instance = archive.LocalScribe.create_with_router_for_user(1, 'avatar')
        self.assertIsInstance(local_scribe_instance, archive.LocalScribe)


class LocalScribeSaveTest(base.TestCase):

    def setUp(self):
        self.local_scribe = archive.LocalScribe(1, self.mock.MagicMock(file_path='/some/path'))

    @base.mock.patch('app.central_files.archive.shutil')
    @base.mock.patch('app.central_files.archive.os')
    def test_should_call_os_to_check_if_path_exists(self, os_mock, shutil_mock):
        self.local_scribe.save(self.mock.MagicMock())
        self.assertTrue(os_mock.path.exists.called)

    @base.mock.patch('app.central_files.archive.shutil')
    @base.mock.patch('app.central_files.archive.os')
    def test_should_call_os_to_makedirs_if_path_dont_exists(self, os_mock, shutil_mock):
        path_mock = self.mock.MagicMock
        exists_mock = self.mock.MagicMock()
        exists_mock.return_value = False
        path_mock.exists = exists_mock
        os_mock.path = path_mock
        self.local_scribe.save(self.mock.MagicMock())
        self.assertTrue(os_mock.makedirs.called)

    @base.mock.patch('app.central_files.archive.shutil')
    @base.mock.patch('app.central_files.archive.os')
    def test_should_call_shutil_to_move_file_to_router_path(self, os_mock, shutil_mock):
        self.local_scribe.save(self.mock.MagicMock())
        self.assertTrue(shutil_mock.move.called)

    @base.mock.patch('app.central_files.archive.shutil')
    @base.mock.patch('app.central_files.archive.os')
    def test_should_return_router_file_path(self, os_mock, shutil_mock):
        result = self.local_scribe.save(self.mock.MagicMock())
        self.assertTrue(result, '/some/path')

    def tearDown(self):
        self.local_scribe = None


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
