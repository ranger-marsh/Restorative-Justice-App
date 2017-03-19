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

    def create_table(self):
        cursor = self.db.cursor()
        cursor.execute('''
                        CREATE TABLE cases(id INTEGER PRIMARY KEY, case_number TEXT, case_date TEXT,
                        incident TEXT, age TEXT, arrest_type TEXT, name TEXT, address TEXT, dob TEXT,
                        phone TEXT, race TEXT, sex  TEXT, district TEXT)
                    ''')
        self.db.commit()



    def close_db(self):
        self.db.close()
