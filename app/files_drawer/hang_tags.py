from app import config as config_module

config = config_module.get_config()


class FilePath(object):

    def __init__(self, user_id):
        self._user_id = user_id

    @property
    def user_id(self):
        return self._user_id

    @property
    def path(self):
        raise NotImplemented


class AvatarFilePath(FilePath):

    def __init__(self, user_id):
        super(AvatarFilePath, self).__init__(user_id)
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
