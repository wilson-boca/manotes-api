from tests import base
from app import models


class AbstractModelUpdateFromJsonTest(base.TestCase):

    @base.TestCase.mock.patch('app.models.AbstractModel.set_values')
    @base.TestCase.mock.patch('app.models.AbstractModel.save_db')
    def test_should_call_save_db(self, save_db_mock, set_values_mock):
        instance = self.mock.MagicMock()
        abstract_model = models.AbstractModel()
        abstract_model.update_from_json({'oi': 'oi'})
        self.assertTrue(save_db_mock.called)


    @base.TestCase.mock.patch('app.models.AbstractModel.set_values')
    @base.TestCase.mock.patch('app.models.AbstractModel.save_db')
    def test_should_call_set_values(self, save_db_mock, set_values_mock):
        instance = self.mock.MagicMock()
        abstract_model = models.AbstractModel()
        abstract_model.update_from_json({'oi': 'oi'})
        self.assertTrue(set_values_mock.called)


class AbstractModelSaveDbTest(base.TestCase):

    @base.TestCase.mock.patch('app.models.db')
    def test_should_call_session_to_commit(self, db_mock):
        session = self.mock.MagicMock()
        db_mock.session = session

        qm = models.AbstractModel()
        qm.save_db()
        self.assertTrue(session.commit.called)

    @base.TestCase.mock.patch('app.models.db')
    def test_should_call_session_to_add(self, db_mock):
        session = self.mock.MagicMock()
        db_mock.session = session

        qm = models.AbstractModel()
        qm.save_db()
        self.assertTrue(session.add.called)


class AbstractModelDeleteDbTest(base.TestCase):

    @base.TestCase.mock.patch('app.models.db')
    def test_should_call_session_to_commit(self, db_mock):
        session = self.mock.MagicMock()
        db_mock.session = session

        abstract_model = models.AbstractModel()
        abstract_model.delete_db()
        self.assertTrue(session.commit.called)

    @base.TestCase.mock.patch('app.models.db')
    def test_should_call_session_to_delete(self, db_mock):
        session = self.mock.MagicMock()
        db_mock.session = session

        abstract_model = models.AbstractModel()
        abstract_model.delete_db()
        self.assertTrue(session.delete.called)


class AbstractModelCreateFromJson(base.TestCase):

    @base.TestCase.mock.patch('app.models.db')
    @base.TestCase.mock.patch('app.models.AbstractModel.save_db')
    @base.TestCase.mock.patch('app.models.AbstractModel.set_values')
    def test_should_call_set_values(self, set_values_mock, save_db_mock, db_mock):
        session = self.mock.MagicMock()
        db_mock.session = session

        abstract_model = models.AbstractModel()
        abstract_model.create_from_json({'key': 'value'})
        self.assertTrue(set_values_mock.called)

    @base.TestCase.mock.patch('app.models.db')
    @base.TestCase.mock.patch('app.models.AbstractModel.save_db')
    @base.TestCase.mock.patch('app.models.AbstractModel.set_values')
    def test_should_call_save_db(self, set_values_mock, save_db_mock, db_mock):
        session = self.mock.MagicMock()
        db_mock.session = session

        abstract_model = models.AbstractModel()
        abstract_model.create_from_json({'key': 'value'})
        self.assertTrue(set_values_mock.called)
