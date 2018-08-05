import shutil
import os
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
            return LocalFile(user_id, router)
        if config.PRODUCTION:
            return S3File()
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
        file_path_to_save = self.router.file_path
        if not os.path.exists(file_path_to_save):
            os.makedirs(file_path_to_save)
        shutil.move(file, file_path_to_save)
        return file_path_to_save


class S3File(File):
    def save(self, file):
        pass


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
        self._path = '{}/{}'.format(config.FILE_STORAGE_PATH, self.user_id)

    @property
    def path(self):
        return self._path

    @property
    def file_path(self):
        return '{}/{}'.format(self.path, 'avatar.png')

    @classmethod
    def create_for_user(cls, user_id):
        return cls(user_id)
