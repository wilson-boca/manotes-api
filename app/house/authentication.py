class EnemDoorman(object):

    class UserNotExists(Exception):
        pass

    @classmethod
    def authenticate(cls, credentials):
        if credentials['username'] == 'breno':
            if credentials['password'] == '12345':
                return True
            return False
        raise cls.UserNotExists('The user {} not exists')