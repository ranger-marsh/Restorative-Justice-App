import os
import sqlite3
from pathlib import Path
from AppDb import AppDb


class TestAppDb:

    def setup_method(self, method):
        self.db = AppDb(test=True, test_path='{}/test_data/temp_db'.format(os.getcwd()))

    def teardown_method(self, method):
        self.db.close_db()
        os.remove('{}/test_data/temp_db'.format(os.getcwd()))

    def test_db_creation(self):
        db_file = Path('{}/test_data/temp_db'.format(os.getcwd()))
        assert db_file.is_file()

    def test_create_table(self):
        expected = ['id', 'case_number', 'case_date', 'incident', 'ori', 'age', 'arrest_type',
                    'name', 'address', 'apartment', 'city', 'state', 'dob', 'phone', 'race', 'sex',
                    'subject_type', 'district', 'status']
        self.db.create_table()
        self.db.close_db()
        db = sqlite3.connect('{}/test_data/temp_db'.format(os.getcwd()))
        cursor = db.execute('select * from cases')
        headers = [description[0] for description in cursor.description]
        db.close()
        assert headers == expected

    def test_write_row(self):
        test_row = ['1', '2', '3', '4', '5', '6', '7', '8',
                    '9', '10', '11', '12', '13', '14', '15', '16', '17']

        test_many = list()
        test_many.append(test_row)
        test_many.append(test_row)
        test_many.append(test_row)

        self.db.create_table()
        self.db.insert_rows(test_many)
        self.db.close_db()
        db = sqlite3.connect('{}/test_data/temp_db'.format(os.getcwd()))
        cursor = db.execute('select * from cases')
        assert cursor.fetchone()[1:] == ('1', '2', '3', '4', '5', '6', '7', '8',
                                         '9', '10', '11', '12', '13', '14', '15', '16', '17', 0)  # [0] is the row id
        assert cursor.fetchone()[0] == 2  # test row id increments.
        assert cursor.fetchone()[0] == 3  # test row id increments.

    def test_query_db(self):
        test_row = ['1', '2', '3', '4', '5', '6', '7', '8',
                    '9', '10', '11', '12', '13', '14', '15', '16', '17']

        test_many = list()
        test_many.append(test_row)
        test_many.append(test_row)
        test_many.append(test_row)
        self.db.create_table()
        self.db.insert_rows(test_many)
        assert len(self.db.query_db(0)) == 3
        assert self.db.query_db(0)[0] == (1, '1', '2', '3', '4', '5', '6', '7', '8',
                                          '9', '10', '11', '12', '13', '14', '15', '16', '17', 0)
        assert self.db.query_db(0)[1] == (2, '1', '2', '3', '4', '5', '6', '7', '8',
                                          '9', '10', '11', '12', '13', '14', '15', '16', '17', 0)
        self.db.close_db()

    def test_change_status(self):
        test_row = ['1', '2', '3', '4', '5', '6', '7', '8',
                    '9', '10', '11', '12', '13', '14', '15', '16', '17']

        test_many = list()
        test_many.append(test_row)
        test_many.append(test_row)
        test_many.append(test_row)
        self.db.create_table()
        self.db.insert_rows(test_many)
        self.db.update_status(1, 3)
        assert len(self.db.query_db(1)) == 1
        self.db.update_status(10, 3)
        assert len(self.db.query_db(11)) == 1
        self.db.update_status(100, 3)
        assert len(self.db.query_db(111)) == 1
        assert len(self.db.query_db(1)) == 0
        assert len(self.db.query_db(11)) == 0
        self.db.close_db()

    def test_check_membership(self):
        test_rowa = ['2015-57325012', '10/11/2015', 'Drug Incident/Investigation', 'NQ4054983', '26', '', 'Oliver Coleman',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'Central']

        test_rowb = ['2017-57325012', '10/11/2015', 'Drug Incident/Investigation', 'NQ4054983', '26', '', 'Oliver Coleman',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'Central']

        test_rowc = ['2017-57325012', '10/11/2015', 'Drug Incident/Investigation', 'NQ4054983', '26', '', 'Scott Frasier',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'Central']

        test_rowd = ['2019-57325012', '10/11/2015', 'Drug Incident/Investigation', 'NQ4054983', '26', '', 'Rupert Frasier',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'Central']

        test_many = list()
        test_many.append(test_rowa)
        test_many.append(test_rowb)
        test_many.append(test_rowc)

        self.db.create_table()
        self.db.insert_rows(test_many)
        assert self.db.query_db(0)[0] == (1, '2015-57325012', '10/11/2015', 'Drug Incident/Investigation', 'NQ4054983', '26', '', 'Oliver Coleman',
                                          '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'Central', 0)
        self.db.check_membership(test_rowa)
        assert self.db.query_db(0)[0] != (1, '2015-57325012', '10/11/2015', 'Drug Incident/Investigation', 'NQ4054983', '26', '', 'Oliver Coleman',
                                          '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'Central', 0)
