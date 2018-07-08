from tests import base
from app.house import residents


class UserTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_create_with_id(self, repository_mock):
        user_mocked = self.mock.MagicMock('something')
        user_mocked.id = 1
        repository_mock.one_or_none.return_value = user_mocked
        user_created = residents.User.create_with_id(1)
        self.assertTrue(isinstance(user_created, residents.User))

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_create_with_id_raise_not_found(self, repository_mock):
        repository_mock.one_or_none.return_value = None
        with self.assertRaises(residents.NotFound):
            residents.User.create_with_id(1)

    def test_create_with_instance(self):
        instance_mocked = self.mock.MagicMock('something')
        instance_mocked.id = 1
        user_created = residents.User.create_with_instance(instance_mocked)
        self.assertTrue(isinstance(user_created, residents.User))

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_create_with_token(self, repository_mock):
        user_mocked = self.mock.MagicMock('something')
        user_mocked.id = 1
        repository_mock.one_or_none.return_value = user_mocked
        user_created = residents.User.create_with_token('UsErRToKeN')
        self.assertTrue(isinstance(user_created, residents.User))

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_create_with_token_raise_not_found(self, repository_mock):
        repository_mock.one_or_none.return_value = None
        with self.assertRaises(residents.NotFound):
            residents.User.create_with_token('UsErRToKeN')

    @base.TestCase.mock.patch('app.house.residents.User.repository')
    def test_create_with_id_raise_not_found(self, repository_mock):
        repository_mock.one_or_none.return_value = None
        with self.assertRaises(residents.NotFound):
            residents.User.create_with_id(1)
