import os
from importlib import import_module # WTF?????????


class Config(object):
    DEBUG = False
    TESTING = False
    DEVELOPMENT = False
    ENVIRONMENT = 'development'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQLALCHEMY_RECORD_QUERIES = True # WTF?????


class TestingConfig(Config):
    TESTING = True
    KEY_ON_TEST = 'KEY ON TEST' # WTF????????
    ENVIRONMENT = 'test'


class ConfigClassNotFound(Exception):
    pass


def get_config():
    config_imports = os.environ['APP_SETTINGS'].split('.')
    config_class_name = config_imports[-1]
    config_module = import_module('.'.join(config_imports[:-1]))
    config_class = getattr(config_module, config_class_name, None)
    if not config_class:
        raise ConfigClassNotFound('Could not find a config class in {}'.format(os.environ['APP_SETTINGS']))
    return config_class
