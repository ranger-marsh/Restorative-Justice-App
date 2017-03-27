import os
import sqlite3
from pathlib import Path

import database_handler

PATH = '{}/test_data/temp_db'.format(os.getcwd())


class Test_database_handler_filtering:

    def teardown_method(self, method):
        db = Path(PATH)
        if db.is_file():
            os.remove(PATH)

    def test_update_status(self):
        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        database_handler.create_table(cursor)

        test_row = ['1', '2', '3', '4', '5', '6', '7', '8',
                    '9', '10', '11', '12', '13', '14', '15', '16', '17']

        test_row1 = ['10', '2', '3', '4', '5', '6', '7', '8',
                     '9', '10', '11', '12', '13', '14', '15', '16', '17']

        database_handler.insert_rows(cursor, [test_row, test_row1])

        assert len(database_handler.query_status(cursor, 0)) == 2

        database_handler.update_status(cursor, 1, 1)
        assert len(database_handler.query_status(cursor, 1)) == 1

        database_handler.update_status(cursor, 10, 1)
        assert len(database_handler.query_status(cursor, 11)) == 1

        assert len(database_handler.query_status(cursor, 0)) == 1

    def test_filter_offenses(self):

        test_row = [4, '2019-57325012', '10/11/2015', 'test', 'NQ4054983', '26', '', 'Rupert Frasier',
                    '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968',
                    'White', 'Male', '', 'central', 0]

        test_rowa = [4, '2019-57325012', '10/11/2015', 'NO', 'NQ4054983', '26', '', 'Rupert Frasier',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968',
                     'White', 'Male', '', 'central', 0]

        assert not database_handler.filter_offenses(test_row, set(['test']))
        assert database_handler.filter_offenses(test_rowa, set(['test']))

    def test_filter_districs(self):
        test_row = [4, '2019-57325012', '10/11/2015', 'test', 'NQ4054983', '26', 'cited', 'Rupert Frasier',
                    '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968',
                    'White', 'Male', '', 'central', 0]

        test_rowa = [4, '2019-57325012', '10/11/2015', 'NO', 'NQ4054983', '26', '', 'Rupert Frasier',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968',
                     'White', 'Male', '', 'task force', 0]

        assert not database_handler.filter_districts(test_row)
        assert database_handler.filter_districts(test_rowa)

    def test_filter_data(self):
        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        database_handler.create_table(cursor)

        test_0 = ['2015-57325012', '10/11/2015', 'valid', 'NQ4054983', '26', 'cited', 'name1',
                  '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central']

        test_1 = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', 'cited', 'name2',
                  '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central']

        test_10 = ['2015-57325012', '10/11/2015', 'valid', 'NQ4054983', '26', 'cited', 'name3',
                   '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'task force']

        test_11 = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', 'cited', 'name4',
                   '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'town of madison']

        rows = [test_0, test_1, test_10, test_11]
        database_handler.insert_rows(cursor, rows)

        assert len(database_handler.query_status(cursor, 0)) == 4
        database_handler.fileter_data(cursor, ['valid'])

        assert len(database_handler.query_status(cursor, 0)) == 1
        assert len(database_handler.query_status(cursor, 1)) == 1
        assert len(database_handler.query_status(cursor, 10)) == 1
        assert len(database_handler.query_status(cursor, 11)) == 1
