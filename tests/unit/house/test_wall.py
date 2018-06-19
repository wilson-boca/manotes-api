from tests import base
from app.house import wall


class NoteTest(base.TestCase):

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
