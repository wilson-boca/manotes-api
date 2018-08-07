import shutil
import os
import secrets
import boto3
from app import config as config_module
from app import exceptions

config = config_module.get_config()


class InvalidEnvironment(Exception):
    pass


class File(object):
    _user_id = None

    @property
    def user_id(self):
        return self._user_id

    @classmethod
    def create_with_environment(cls, user_id, router):
        if config.DEVELOPMENT:
            return S3File(user_id, router)
        if config.PRODUCTION:
            return S3File(user_id, router)
        raise InvalidEnvironment('Could  not instantiate a file class '
                                 'because the environment config is not development or production')

    def save(self, file):
        raise NotImplemented


class LocalFile(File):

    def __init__(self, user_id, router):
        self._user_id = user_id
        if router == 'avatar':
            self._router = AvatarDirectoryRouter.create_for_user(user_id)
        else:
            raise exceptions.InvalidRouter('Please pass a valid router for File')

    @property
    def router(self):
        return self._router

    def save(self, file):
        if not os.path.exists(self.router.path):
            os.makedirs(self.router.path)
        shutil.move(file, self.router.file_path)
        return self.router.file_path


class S3File(File):
    def __init__(self, user_id, router):
        self._user_id = user_id
        self._access_key_id = config.S3_AWS_ACCESS_KEY_ID
        self._secret_access_key = config.S3_AWS_SECRET_ACCESS_KEY
        self._bucket_name = config.AVATAR_BUCKET_NAME
        session = boto3.session.Session()
        self._s3_client = boto3.client(
            's3',
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.secret_access_key,
        )
        if router == 'avatar':
            self._router = AvatarDirectoryRouter.create_for_user(user_id)
        else:
            raise exceptions.InvalidRouter('Please pass a valid router for File')

    @property
    def access_key_id(self):
        return self._access_key_id

    @property
    def secret_access_key(self):
        return self._secret_access_key

    @property
    def router(self):
        return self._router

    @property
    def bucket_name(self):
        return self._bucket_name

    @property
    def s3_client(self):
        return self._s3_client

    def save(self, file):
        self.s3_client.upload_file(file, self.bucket_name, self.router.file_name)


class DirectoryRouter(object):

    def __init__(self, user_id):
        self._user_id = user_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def path(self):
        raise NotImplemented


class AvatarDirectoryRouter(DirectoryRouter):

    def __init__(self, user_id):
        super(AvatarDirectoryRouter, self).__init__(user_id)
        self._path = '{}/{}/'.format(config.FILE_STORAGE_PATH, config.AVATAR_BUCKET_NAME)
        self._bucket_name = config.AVATAR_BUCKET_NAME
        self._hash = secrets.token_hex(8)

    @property
    def path(self):
        return self._path

    @property
    def file_path(self):
        return '{}avatar-{}.png'.format(self.path, self._hash)

    @property
    def file_name(self):
        return 'avatar-{}.png'.format(self._hash)

    @property
    def bucket_name(self):
        return self._bucket_name

    @property
    def hash(self):
        return self._hash

    @classmethod
    def create_for_user(cls, user_id):
        return cls(user_id)
