from tests import base
from app import models


class AbstractModelTest(base.TestCase):

    @base.TestCase.mock.patch('app.models.AbstractModel.set_values')
    @base.TestCase.mock.patch('app.models.AbstractModel.save_db')
    def test_update_from_json(self, save_db_mock, set_values_mock):
        instance = self.mock.MagicMock()
        abstract_model = models.AbstractModel()
        abstract_model.update_from_json({'oi': 'oi'})
        self.assertTrue(save_db_mock.called)
        self.assertTrue(set_values_mock.called)

    @base.TestCase.mock.patch('app.models.db')
    def test_save_db_add(self, db_mock):
        session = self.mock.MagicMock()
        db_mock.session = session

        qm = models.AbstractModel()
        qm.save_db()
        self.assertTrue(session.commit.called)
        self.assertTrue(session.add.called)

    @base.TestCase.mock.patch('app.models.db')
    def test_delete_db(self, db_mock):
        session = self.mock.MagicMock()
        db_mock.session = session

        abstract_model = models.AbstractModel()
        abstract_model.delete_db()
        self.assertTrue(session.commit.called)
        self.assertTrue(session.delete.called)

    @base.TestCase.mock.patch('app.models.db')
    @base.TestCase.mock.patch('app.models.AbstractModel.save_db')
    @base.TestCase.mock.patch('app.models.AbstractModel.set_values')
    def test_create_from_json(self, set_values_mock, save_db_mock, db_mock):
        session = self.mock.MagicMock()
        db_mock.session = session

        abstract_model = models.AbstractModel()
        abstract_model.create_from_json({'key': 'value'})
        self.assertTrue(set_values_mock.called)
        self.assertTrue(save_db_mock.called)
