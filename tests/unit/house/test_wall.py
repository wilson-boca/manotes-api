from tests import base
from app.house import wall


class NoteTest(base.TestCase):

    @base.TestCase.mock.patch('app.house.wall.Note.repository.one_or_none')
    def setUp(self, one_or_none_mock):
        one_or_none_mock = self.mock.MagicMock()
        self.note = wall.Note.create_with_id(1)

    @base.TestCase.mock.patch('app.house.wall.Note.repository.one_or_none')
    @base.TestCase.mock.patch('app.house.wall.Note.repository')
    def test_create_with_id(self, repository_mock, one_or_none_mock):
        repository_mock = self.mock.MagicMock()
        created_note = wall.Note.create_with_id(1)
        self.assertTrue(one_or_none_mock.called)
        self.assertTrue(isinstance(created_note, wall.Note))

    @base.TestCase.mock.patch('app.house.wall.Note.repository.one_or_none')
    @base.TestCase.mock.patch('app.house.wall.Note.repository')
    def test_create_with_id_raise_not_found_if_none(self, repository_mock, one_or_none_mock):
        repository_mock = self.mock.MagicMock()
        one_or_none_mock.return_value = None
        with self.assertRaises(wall.Note.NotFound):
            wall.Note.create_with_id(1)

    @base.TestCase.mock.patch('app.house.wall.Note.repository')
    def test_create_with_instance(self, repository_mock):
        repository_mock = self.mock.MagicMock()
        instance_mock = self.mock.MagicMock()
        created_note = wall.Note.create_with_instance(instance_mock)
        self.assertTrue(isinstance(created_note, wall.Note))

    @base.TestCase.mock.patch('app.house.wall.Note.repository.create_from_json')
    def test_create_new(self, create_from_json_mock):
        instance_mock = self.mock.MagicMock()
        created_note = wall.Note.create_new(instance_mock)
        self.assertTrue(create_from_json_mock.called)

    @base.TestCase.mock.patch('app.house.wall.Note.repository.filter')
    def test_list(self, filter_mock):
        instance_mock = self.mock.MagicMock()
        notes = wall.Note.list()
        self.assertTrue(filter_mock.called)

    def test_update(self):
        self.note.db_instance.update_from_json = self.mock.MagicMock()
        self.note.update({'key': 'value'})
        self.assertTrue(self.note.db_instance.update_from_json.called)

    def tearDown(self):
        self.note = {}
