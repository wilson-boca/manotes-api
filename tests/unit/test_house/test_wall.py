from tests import base
from app import exceptions
from app.house import wall


class NoteTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.wall.Note.repository')
    def test_create_with_id_should_call_repository_one_or_none(self, repository_mock):
        wall.Note.create_with_id(1)
        self.assertTrue(repository_mock.one_or_none)

    @base.TestCase.mock.patch('app.house.wall.Note.repository')
    def test_create_with_id_should_return_instance(self, repository_mock):
        note_mock = self.mock.MagicMock()
        repository_mock.one_or_none.return_value = note_mock
        created_note = wall.Note.create_with_id(1)
        self.assertTrue(isinstance(created_note, wall.Note))

    @base.TestCase.mock.patch('app.house.wall.Note.repository.one_or_none')
    def test_create_with_id_should_raise_not_found_if_id_dont_exists(self, one_or_none_mock):
        one_or_none_mock.return_value = None
        with self.assertRaises(exceptions.NotFound):
            wall.Note.create_with_id(1)

    def test_create_with_instance_should_return_instance(self):
        instance_mock = self.mock.MagicMock()
        created_note = wall.Note.create_with_instance(instance_mock)
        self.assertTrue(isinstance(created_note, wall.Note))

    @base.TestCase.mock.patch('app.house.wall.Note.repository.one_or_none')
    def test_create_for_user_should_call_repository_one_or_none(self, one_or_none_mock):
        note_mock = self.mock.MagicMock()
        note_mock.user_id = 1
        one_or_none_mock.return_value = note_mock
        created_note = wall.Note.create_for_user(1, 1)
        self.assertTrue(one_or_none_mock.called)
        self.assertTrue(isinstance(created_note, wall.Note))

    @base.TestCase.mock.patch('app.house.wall.Note.repository.one_or_none')
    def test_create_for_user_should_call_return_instance(self, one_or_none_mock):
        note_mock = self.mock.MagicMock()
        note_mock.user_id = 1
        one_or_none_mock.return_value = note_mock
        created_note = wall.Note.create_for_user(1, 1)
        self.assertTrue(isinstance(created_note, wall.Note))

    @base.TestCase.mock.patch('app.house.wall.Note.repository.one_or_none')
    def test_create_for_user_should_return_not_found_if_id_dont_exists(self, one_or_none_mock):
        note_mock = self.mock.MagicMock()
        one_or_none_mock.return_value = None
        with self.assertRaises(exceptions.NotFound):
            wall.Note.create_for_user(1, 1)

    @base.TestCase.mock.patch('app.house.wall.Note.repository.one_or_none')
    def test_create_for_user_return_not_mine_if_found_but_user_id_different(self, one_or_none_mock):
        note_mock = self.mock.MagicMock()
        note_mock.user_id = 1
        one_or_none_mock.return_value = note_mock
        with self.assertRaises(exceptions.NotMine):
            wall.Note.create_for_user(1, 2)

    @base.TestCase.mock.patch('app.house.wall.Note.repository.create_from_json')
    def test_create_new_should_call_repository_create_from_json(self, create_from_json_mock):
        instance_mock = self.mock.MagicMock()
        created_note = wall.Note.create_new(instance_mock)
        self.assertTrue(create_from_json_mock.called)

    @base.TestCase.mock.patch('app.house.wall.Note.repository.create_from_json')
    def test_create_new_should_return_created_instance(self, create_from_json_mock):
        instance_mock = self.mock.MagicMock()
        create_from_json_mock.return_value = instance_mock
        created_note = wall.Note.create_new(instance_mock)
        self.assertTrue(isinstance(created_note, wall.Note))

    @base.TestCase.mock.patch('app.house.wall.Note.repository.filter')
    def test_list_for_user_should_call_repository_filter(self, filter_mock):
        wall.Note.list_for_user(1)
        self.assertTrue(filter_mock.called)

    @base.TestCase.mock.patch('app.house.wall.Note.repository.filter')
    def test_list_for_user_should_return_list(self, filter_mock):
        filter_mock.return_value = []
        notes = wall.Note.list_for_user(1)
        self.assertTrue(isinstance(notes, list))

    def test_update_should_call_repository_update_from_json(self):
        note = wall.Note.create_with_instance(self.mock.MagicMock())
        note.update({'key': 'value'})
        self.assertTrue(note.db_instance.update_from_json.called)
