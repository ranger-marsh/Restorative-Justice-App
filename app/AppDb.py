import sqlite3
import os


class AppDb:

    def __init__(self, test=False, test_path=''):
        if not test:
            if os.isfile('app_files/app_db'):
                self.db = sqlite3.connect('app_files/app_db')
            else:
                self.db = sqlite3.connect('app_files/app_db')
                create_table()
        else:
            self.db = sqlite3.connect(test_path)

        self.cursor = self.db.cursor()

    def create_table(self):

        self.cursor.execute('''
                        CREATE TABLE cases(id INTEGER PRIMARY KEY, case_number TEXT, case_date TEXT,
                        incident TEXT, ori TEXT, age TEXT, arrest_type TEXT, name TEXT,
                        address TEXT, apartment TEXT, city TEXT, state TEXT, dob TEXT, phone TEXT,
                        race TEXT, sex TEXT, district TEXT, status INTEGER)
                    ''')
        self.db.commit()

    def insert_rows(self, row):
        self.cursor.executemany(
            '''INSERT INTO cases(case_number, case_date, incident, ori, age, arrest_type, name,
                                address, apartment, city, state, dob, phone, race, sex, district,status)
                                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', row)
        self.db.commit()

    def close_db(self):
        self.db.close()
