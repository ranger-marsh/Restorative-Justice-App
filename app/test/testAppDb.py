import os
import sqlite3
from pathlib import Path
from AppDb import *


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
        expected = ['id', 'case_number', 'case_date', 'incident', 'age', 'arrest_type',
                    'name', 'address', 'dob', 'phone', 'race', 'sex', 'district']
        self.db.create_table()
        self.db.close_db()
        db = connection = sqlite3.connect('{}/test_data/temp_db'.format(os.getcwd()))
        cursor = connection.execute('select * from cases')
        headers = [description[0] for description in cursor.description]
        db.close()
        assert headers == expected
