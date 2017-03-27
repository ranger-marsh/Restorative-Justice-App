import sqlite3


def create_table(cursor):
    cursor.execute('''
                    CREATE TABLE cases(id INTEGER PRIMARY KEY, case_number TEXT, case_date TEXT,
                    incident TEXT, ori TEXT, age TEXT, arrest_type TEXT CHECK (length(arrest_type ) > 0), name TEXT,
                    address TEXT, apartment TEXT, city TEXT, state TEXT, dob TEXT, phone TEXT,
                    race TEXT, sex TEXT, subject_type TEXT, district TEXT, status INTEGER DEFAULT 0)
                    ''')
    return None


def insert_rows(cursor, row):

    cursor.executemany(
        '''INSERT OR IGNORE INTO cases(case_number, case_date, incident, ori, age, arrest_type, name,
            address, apartment, city, state, dob, phone, race, sex, subject_type, district)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', row
    )

    return None


def query_status(cursor, status):
    cursor.execute("SELECT * FROM cases WHERE status=?", (status,))
    return cursor.fetchall()


def update_status(cursor, status, row_id):
    curr_status = cursor.execute(
        "SELECT * FROM cases WHERE id=?", [(row_id)]).fetchone()[-1]
    status += curr_status
    cursor.execute("UPDATE cases SET status=? WHERE id=?", (status, row_id))
    return None


def offense_types(cursor):
    results = query_status(cursor, 0)
    incidents = set([row[3] for row in results])
    return incidents


def fileter_data(cursor, offense_list):
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
    if row[3] not in offense_list:
        return True
    return False


def filter_districts(row):
    districts = set(['east', 'central', 'west', 'north', 'south'])
    if row[17] not in districts:
        return True
    return False


def main():
    pass

if __name__ == '__main__':
    main()
