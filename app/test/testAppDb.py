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
                    'name', 'address', 'apartment', 'city', 'state', 'dob', 'phone', 'race', 'sex', 'district','status']
        self.db.create_table()
        self.db.close_db()
        db = sqlite3.connect('{}/test_data/temp_db'.format(os.getcwd()))
        cursor = db.execute('select * from cases')
        headers = [description[0] for description in cursor.description]
        db.close()
        assert headers == expected

    def test_write_row(self):
        test_row = ['1', '2', '3', '4', '5', '6', '7', '8',
                    '9', '10', '11', '12', '13', '14', '15', '16', 0]
        self.db.create_table()
        self.db.insert_row(test_row)
        self.db.insert_row(test_row)
        self.db.close_db()
        db = sqlite3.connect('{}/test_data/temp_db'.format(os.getcwd()))
        cursor = db.execute('select * from cases')
        assert cursor.fetchone()[1:] == tuple(test_row) # [0] is the row id
        assert cursor.fetchone()[0] == 2 # test row id increments.
