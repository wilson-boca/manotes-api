from app import config as config_module

config = config_module.get_config()


class InvalidEnvironment(Exception):
    pass


class File(object):
    _user_id = None

    @property
    def user_id(self):
        return self._user_id

    @classmethod
    def create_with_environment(cls, user_id):
        if config.DEVELOPMENT:
            return LocalFile(config.FILE_STORAGE_PATH, user_id)
        if config.PRODUCTION:
            return S3File()
        raise InvalidEnvironment('Could  not instantiate a file class '
                                 'because the environment config is not development or production')

    def save(self, file):
        raise NotImplemented


class LocalFile(File):

    def __init__(self, storage_path, user_id):
        self._storage_path = storage_path
        self._user_id = user_id

    def save(self, file):
        pass


class S3File(File):
    def save(self, file):
        pass
