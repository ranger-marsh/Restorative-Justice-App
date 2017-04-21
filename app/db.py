import sqlite3
import create_database

PATH = '{}/test_data/temp_db.sqlite3'.format(os.getcwd())


def create_tables():
    db = sqlite3.connect(PATH)
    cursor = db.cursor()
    create_database.create_tables(cursor)

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    assert cursor.fetchall() == [('cases',), ('status',),
                                 ('arrestee',), ('arrest',), ('contact',)]


def main():
    create_tables()

if __name__ == '__main__':
    main()
