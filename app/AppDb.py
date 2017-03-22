import sqlite3
import csv
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

    def open_csv(self, path):
        with open(path) as csvfile:
            reader = list(csv.reader(csvfile, delimiter=','))
            rows = [[val.strip().lower() for val in row] for row in reader[1:]]
        return rows

    def create_table(self):

        self.cursor.execute('''
                        CREATE TABLE cases(id INTEGER PRIMARY KEY, case_number TEXT, case_date TEXT,
                        incident TEXT, ori TEXT, age TEXT, arrest_type TEXT, name TEXT,
                        address TEXT, apartment TEXT, city TEXT, state TEXT, dob TEXT, phone TEXT,
                        race TEXT, sex TEXT, district TEXT, status INTEGER DEFAULT 0)
                    ''')
        self.db.commit()

    def insert_rows(self, row):
        self.cursor.executemany(
            '''INSERT INTO cases(case_number, case_date, incident, ori, age, arrest_type, name,
                                address, apartment, city, state, dob, phone, race, sex, district)
                                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', row)
        self.db.commit()

    def query_db(self, query):
        sql = "SELECT * FROM cases WHERE status=?"
        self.cursor.execute(sql, [(query)])
        return self.cursor.fetchall()

    def update_status(self, status, row_id):
        curr_status = self.cursor.execute(
            "SELECT * FROM cases WHERE id=?", [(row_id)]).fetchone()[-1]
        status += curr_status
        self.cursor.execute("UPDATE cases SET status=? WHERE id=?", (status, row_id))

    def close_db(self):
        self.db.close()
