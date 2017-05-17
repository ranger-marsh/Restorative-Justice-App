#!/usr/bin/env python3

"""
Functions for using the adding, manipulating and consuming data with
sqlite3. The table is created that does not allow duplicates or empty
empty strings in key columns. It also filters data based on user
specified values.
"""

import sqlite3


def create_table(cursor):
    # Table only accepts unique cases if the case number and name are already
    # in the database it is not entered. Also cases without a disposition are
    # not entered this is based on arrest type.
    cursor.execute('''
                    CREATE TABLE cases(id INTEGER PRIMARY KEY, case_number TEXT, case_date TEXT,
                    incident TEXT, ori TEXT, age TEXT, arrest_type TEXT CHECK (length(arrest_type ) > 0),
                    name TEXT, address TEXT, apartment TEXT, city TEXT, state TEXT, zip Text, dob TEXT, phone TEXT,
                    race TEXT, sex TEXT, subject_type TEXT, district TEXT, status INTEGER DEFAULT 0,
                    UNIQUE(case_number , name))
                    ''')
    return None


def insert_rows(cursor, row):

    cursor.executemany(
        '''INSERT OR IGNORE INTO cases(case_number, case_date, incident, ori, age, arrest_type, name,
            address, apartment, city, state, zip, dob, phone, race, sex, subject_type, district)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', row
    )

    return None


def query_status(cursor, status):
    cursor.execute("SELECT * FROM cases WHERE status=?", (status,))
    return cursor.fetchall()


def update_status(cursor, status, row_id):
    # status is used as a filter.
    curr_status = cursor.execute(
        "SELECT * FROM cases WHERE id=?", [(row_id)]).fetchone()[-1]
    status += curr_status
    cursor.execute("UPDATE cases SET status=? WHERE id=?", (status, row_id))
    return None


def offense_types(cursor):
    # Returns a list of offenses of the current run.
    results = query_status(cursor, 0)
    incidents = set([row[3] for row in results])
    return incidents


def receipt(cursor):
    # Get the rows that where filtered out selecting the most recent first.
    cursor.execute("SELECT * FROM cases WHERE status < 100")
    results = [[row[1], row[7], row[3], row[18]] for row in reversed(cursor.fetchall())]
    return results


def fileter_data(cursor, offense_list):
    # Change the status to filter data later.
    results = query_status(cursor, 0)
    for row in results:
        status = 0
        if filter_offenses(row, offense_list):
            status += 1
        if filter_districts(row):
            status += 10
        if status != 0:
            update_status(cursor, status, row[0])
    return None


def filter_offenses(row, offense_list):
    # offense_list is provided by user through UI.
    if row[3] not in offense_list:
        return True
    return False


def filter_districts(row):
    districts = set(['east', 'central', 'west', 'north', 'south'])
    if row[18] not in districts:
        return True
    return False


def main():
    pass


if __name__ == '__main__':
    main()
