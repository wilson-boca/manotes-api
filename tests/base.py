import unittest, os
from mock import mock

os.environ.update({
    'APP_SETTINGS': 'app.config.TestingConfig',
    'DATABASE_URL': 'postgresql+psycopg2://manotes:manotes@localhost/manotes'
})

from app import initialize


class TestCase(unittest.TestCase):
    mock = mock
