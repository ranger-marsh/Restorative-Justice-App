import os
import sqlite3

import database_handler

PATH = '{}/test_data/temp_db.sqlite3'.format(os.getcwd())


class Test_database_handler_insertions:

    def teardown_method(self, method):
        os.remove(PATH)

    def test_no_null_arrest_types(self):
        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        database_handler.create_table(cursor)

        notnull = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', 'cited',
                   'Oliver Coleman', '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998',
                   '63-(829)189-2968', 'White', 'Male', '', 'central']

        null = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', '', 'Oliver Coleman',
                '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968',
                'White', 'Male', '', 'central']

        rows = [notnull, null]

        database_handler.insert_rows(cursor, rows)
        inserted = database_handler.query_status(cursor, 0)

        assert len(inserted) == 1
        assert inserted[0][1:-1] == tuple(notnull)

    def test_insert_unique(self):
        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        database_handler.create_table(cursor)

        name1 = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', 'cited',
                 'Oliver Coleman', '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998',
                 '63-(829)189-2968', 'White', 'Male', '', 'central']

        name2 = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', 'cited', 'different name',
                 '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968',
                 'White', 'Male', '', 'central']

        name3 = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', 'cited', 'different name',
                 '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968',
                 'White', 'Male', '', 'central']

        rows = [name1, name2, name3, name1]

        database_handler.insert_rows(cursor, rows)
        inserted = database_handler.query_status(cursor, 0)

        assert len(inserted) == 2
