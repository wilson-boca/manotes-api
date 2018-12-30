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


class AbstractInitTest(base.TestCase):

    def test_has_user_id(self):
        pass

    def test_has_router(self):
        pass


class AbstractScribeSaveTest(base.TestCase):

    def test_should_raise_not_implemented(self):
        abstract_scribe = archive.AbstractScribe(1, self.mock.MagicMock())
        with self.assertRaises(exceptions.NoImplementationError):
            abstract_scribe.save(file=self.mock.MagicMock())


class AbstractScribeUserIdTest(base.TestCase):

    def test_has_user_id(self):
        abstract_scribe = archive.AbstractScribe(1, self.mock.MagicMock())
        self.assertEqual(1, abstract_scribe.user_id)


class AbstractScribeRouterTest(base.TestCase):

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


class S3ScribeInit(base.TestCase):

    def test_has_access_key_id(self):
        pass

    def test_has_secret_access_key(self):
        pass

    def test_has_bucket_name(self):
        pass

    def test_has_s3_client(self):
        pass


class S3ScribeCreateWithRouterForUserTest(base.TestCase):

    @base.mock.patch('app.central_files.archive.config.S3_AWS_ACCESS_KEY_ID', 'AFDSFASDDFAS')
    @base.mock.patch('app.central_files.archive.config.S3_AWS_SECRET_ACCESS_KEY', 'QERQEWE')
    @base.mock.patch('app.central_files.archive.config.AVATAR_BUCKET_NAME', 'ZXCV')
    @base.mock.patch('app.central_files.archive.AvatarDirectoryRouter.create_for_user', base.mock.MagicMock())
    @base.mock.patch('app.central_files.archive.boto3')
    def test_should_get_call_boto3_to_instantiate_client(self, boto_3_mock):
        archive.S3Scribe.create_with_router_for_user(1, 'avatar')
        boto_3_mock.client.assert_called_with(
            's3',
            aws_access_key_id='AFDSFASDDFAS',
            aws_secret_access_key='QERQEWE',
        )

    @base.mock.patch('app.central_files.archive.config.S3_AWS_ACCESS_KEY_ID', 'AFDSFASDDFAS')
    @base.mock.patch('app.central_files.archive.config.S3_AWS_SECRET_ACCESS_KEY', 'QERQEWE')
    @base.mock.patch('app.central_files.archive.config.AVATAR_BUCKET_NAME', 'ZXCV')
    @base.mock.patch('app.central_files.archive.boto3.client', base.mock.MagicMock())
    def test_should_raise_invalid_router_if_router_is_not_avatar(self):
        with self.assertRaises(exceptions.InvalidRouter):
            archive.S3Scribe.create_with_router_for_user(1, 'qwerty')

    @base.mock.patch('app.central_files.archive.config.S3_AWS_ACCESS_KEY_ID', 'AFDSFASDDFAS')
    @base.mock.patch('app.central_files.archive.config.S3_AWS_SECRET_ACCESS_KEY', 'QERQEWE')
    @base.mock.patch('app.central_files.archive.config.AVATAR_BUCKET_NAME', 'ZXCV')
    @base.mock.patch('app.central_files.archive.boto3.client', base.mock.MagicMock())
    @base.mock.patch('app.central_files.archive.AvatarDirectoryRouter.create_for_user')
    def test_should_call_avatar_directory_router_to_create_for_user(self, create_for_user_mock):
        archive.S3Scribe.create_with_router_for_user(1, 'avatar')
        create_for_user_mock.assert_called_with(1)

    @base.mock.patch('app.central_files.archive.config.S3_AWS_ACCESS_KEY_ID', 'AFDSFASDDFAS')
    @base.mock.patch('app.central_files.archive.config.S3_AWS_SECRET_ACCESS_KEY', 'QERQEWE')
    @base.mock.patch('app.central_files.archive.config.AVATAR_BUCKET_NAME', 'ZXCV')
    @base.mock.patch('app.central_files.archive.boto3.client', base.mock.MagicMock())
    @base.mock.patch('app.central_files.archive.AvatarDirectoryRouter.create_for_user', base.mock.MagicMock())
    def test_should_return_instance(self):
        instance = archive.S3Scribe.create_with_router_for_user(1, 'avatar')
        self.assertIsInstance(instance, archive.S3Scribe)


class S3ScribeSaveTest(base.TestCase):

    def setUp(self):
        self.file_name = 'asd'
        router_mock = self.mock.MagicMock(file_name=self.file_name)
        # TODO: Is this mock right?
        self.s3_scribe = archive.S3Scribe(1, router_mock, 'access_key_id', 'secret_access_key',
                                          'bucket_name', self.mock.MagicMock())

    def test_should_call_s3_client_to_upload_file(self):
        self.s3_scribe.save('image.png')
        self.assertTrue(self.s3_scribe.s3_client.upload_file.called)

    def test_should_raise_upload_file_error_if_upload_file_raises_exception(self):
        self.s3_scribe.s3_client.upload_file = self.mock.MagicMock(side_effect=Exception)
        with self.assertRaises(exceptions.UploadFileError):
            self.s3_scribe.save('image.png')

    def test_should_return_router_file_name(self):
        file_name = self.s3_scribe.save('image.png')
        self.assertEqual(file_name, self.file_name)


class AbstractDirectoryRouterInitTest(base.TestCase):

    def test_has_user_id(self):
        pass


class AvatarDirectoryRouterInitTest(base.TestCase):

    def test_has_path(self):
        pass

    def test_has_bucket_name(self):
        pass

    def test_has_hash(self):
        pass


class AvatarDirectoryRouterFilePathTest(base.TestCase):

    def test_should_use_path_to_construct_file_path(self):
        pass

    def test_should_use_hash_to_construct_file_path(self):
        pass

    def test_should_use_user_id_to_construct_file_path(self):
        pass

    def test_should_return_file_path_with_this_specific_format(self):
        pass


class AvatarDirectoryRouterFileNameTest(base.TestCase):

    def test_should_use_hash_to_construct_file_name(self):
        pass

    def test_should_use_user_id_to_construct_file_name(self):
        pass

    def test_should_return_file_name_with_this_specific_format(self):
        pass


class AvatarDirectoryRouterCreateForUser(base.TestCase):

    def test_should_make_path_with_file_storage_path_and_avatar_bucket_name(self):
        pass

    def test_should_call_security_service_to_generate_a_token(self):
        pass

    def test_should_return_instance(self):
        pass
