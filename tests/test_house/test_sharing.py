from tests import base
from src import config as config_module, exceptions
from src.house import sharing

config = config_module.get_config()


class NoteSharingShareTest(base.TestCase):

    @base.TestCase.mock.patch('src.house.services.NoteService.create_for_user')
    @base.TestCase.mock.patch('src.house.services.UserService.create_with_id')
    @base.TestCase.mock.patch('src.models.NoteSharing.create_from_dict')
    def test_should_call_repository_to_create_from_dict(self, create_from_dict_mock, create_with_id_mock, create_for_user_mock):
        sharing.NoteSharing.share(1, 2, 3)
        self.assertTrue(create_from_dict_mock.called)

    @base.TestCase.mock.patch('src.house.services.NoteService.create_for_user')
    @base.TestCase.mock.patch('src.house.services.UserService.create_with_id')
    @base.TestCase.mock.patch('src.models.NoteSharing.create_from_dict')
    def test_should_call_user_service_to_create_with_id(self, create_from_dict_mock, create_with_id_mock, create_for_user_mock):
        sharing.NoteSharing.share(1, 2, 3)
        create_with_id_mock.assert_called_with(3)

    @base.TestCase.mock.patch('src.house.services.NoteService.create_for_user')
    @base.TestCase.mock.patch('src.house.services.UserService')
    @base.TestCase.mock.patch('src.models.NoteSharing.create_from_dict')
    def test_should_raise_user_not_exists_if_user_service_create_with_id_raises_not_found(self, create_from_dict_mock, user_service_mock, create_for_user_mock):
        user_service_mock.create_with_id = self.mock.MagicMock(side_effect=exceptions.NotFound)
        with self.assertRaises(exceptions.UserNotExists):
            sharing.NoteSharing.share(1, 2, 3)

    @base.TestCase.mock.patch('src.house.services.NoteService.create_for_user')
    @base.TestCase.mock.patch('src.house.services.UserService.create_with_id')
    @base.TestCase.mock.patch('src.models.NoteSharing.create_from_dict')
    def test_should_call_note_service_to_create_for_user(self, create_from_dict_mock, create_with_id_mock, create_for_user_mock):
        sharing.NoteSharing.share(1, 2, 3)
        create_for_user_mock.assert_called_with(2, 1)

    @base.TestCase.mock.patch('src.house.services.NoteService')
    @base.TestCase.mock.patch('src.house.services.UserService.create_with_id')
    @base.TestCase.mock.patch('src.models.NoteSharing.create_from_dict')
    def test_should_raise_note_note_found_if_note_service_create_for_user_raises_not_found(self, create_from_dict_mock, create_with_id_mock, note_service_mock):
        note_service_mock.create_for_user = self.mock.MagicMock(side_effect=exceptions.NotFound)
        with self.assertRaises(exceptions.NoteNotFound):
            sharing.NoteSharing.share(1, 2, 3)

    @base.TestCase.mock.patch('src.house.services.NoteService')
    @base.TestCase.mock.patch('src.house.services.UserService.create_with_id')
    @base.TestCase.mock.patch('src.models.NoteSharing.create_from_dict')
    def test_should_raise_note_note_mine_if_note_service_create_for_user_raises_not_mine(self, create_from_dict_mock, create_with_id_mock, note_service_mock):
        note_service_mock.create_for_user = self.mock.MagicMock(side_effect=exceptions.NotMine)
        with self.assertRaises(exceptions.NoteNotMine):
            sharing.NoteSharing.share(1, 2, 3)
