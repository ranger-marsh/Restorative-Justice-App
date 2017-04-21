import os
import sqlite3
from pathlib import Path

import create_database

PATH = '{}/test_data/temp_db.sqlite3'.format(os.getcwd())


class Test_create_database:

    def teardown_method(self, method):
        db = Path(PATH)
        if db.is_file():
            os.remove(PATH)

    def test_create_case_table(self):
        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        create_database.create_case_table(cursor)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        assert cursor.fetchall() == [('cases',)]

        cursor.execute("SELECT * FROM cases")
        columns = [col[0] for col in cursor.description]
        assert columns == ['id', 'case_number', 'case_date', 'district']

    def test_create_status_table(self):
        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        create_database.create_status_table(cursor)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        assert cursor.fetchall() == [('status',)]

        cursor.execute("SELECT * FROM status")
        columns = [col[0] for col in cursor.description]
        assert columns == ['id', 'case_id', 'arrestee_id', 'approved', 'status', 'completed']

    def test_create_arrestee_table(self):
        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        create_database.create_arrestee_table(cursor)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        assert cursor.fetchall() == [('arrestee',)]

        cursor.execute("SELECT * FROM arrestee")
        columns = [col[0] for col in cursor.description]
        assert columns == ['id', 'case_id', 'name', 'sex', 'race', 'dob', 'age']

    def test_create_arrest_table(self):
        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        create_database.create_arrest_table(cursor)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        assert cursor.fetchall() == [('arrest',)]

        cursor.execute("SELECT * FROM arrest")
        columns = [col[0] for col in cursor.description]
        assert columns == ['id', 'case_id', 'arrestee_id', 'incident_type', 'charge_type']

    def test_create_contact_table(self):
        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        create_database.create_contact_table(cursor)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        assert cursor.fetchall() == [('contact',)]

        cursor.execute("SELECT * FROM contact")
        columns = [col[0] for col in cursor.description]
        assert columns == ['id', 'case_id', 'arrestee_id', 'address', 'phone', 'email']

    def test_create_tables(self):
        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        create_database.create_tables(cursor)

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        assert cursor.fetchall() == [('cases',), ('status',),
                                     ('arrestee',), ('arrest',), ('contact',)]
