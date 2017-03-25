import os
import sqlite3
from pathlib import Path

import database_handler

PATH = '{}/test_data/temp_db'.format(os.getcwd())


class Test_database_handler:

    @classmethod
    def teardown_class(cls):
        os.remove(PATH)

    def test_create_table(self):
        expected = ['id', 'case_number', 'case_date', 'incident', 'ori', 'age', 'arrest_type',
                    'name', 'address', 'apartment', 'city', 'state', 'dob', 'phone', 'race', 'sex',
                    'subject_type', 'district', 'status']

        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        database_handler.create_table(cursor)
        db.commit()
        cursor = db.execute('select * from cases')
        headers = [description[0] for description in cursor.description]
        db.close()
        assert headers == expected

    def test_write_rows(self):
        test_row = ['1', '2', '3', '4', '5', '6', '7', '8',
                    '9', '10', '11', '12', '13', '14', '15', '16', '17']

        test_many = list()
        test_many.append(test_row)
        test_many.append(test_row)
        test_many.append(test_row)

        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        database_handler.insert_rows(cursor, test_many)
        db.commit()
        cursor = db.execute('select * from cases')

        assert cursor.fetchone()[1:] == ('1', '2', '3', '4', '5', '6', '7', '8',
                                         '9', '10', '11', '12', '13', '14', '15', '16', '17', 0)  # [0] is the row id
        assert cursor.fetchone()[0] == 2  # test row id increments.
        assert cursor.fetchone()[0] == 3  # test row id increments.

        db.close()

    def test_query_db(self):
        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        test_row = ['1', '2', '3', '4', '5', '6', '7', '8',
                    '9', '10', '11', '12', '13', '14', '15', '16', '17']

        assert len(database_handler.query_status(cursor, 0)) == 3
        assert database_handler.query_status(cursor, 0)[0] == (1, '1', '2', '3', '4', '5', '6', '7', '8',
                                                               '9', '10', '11', '12', '13', '14', '15', '16', '17', 0)
        assert database_handler.query_status(cursor, 0)[1] == (2, '1', '2', '3', '4', '5', '6', '7', '8',
                                                               '9', '10', '11', '12', '13', '14', '15', '16', '17', 0)
        db.close()

    def test_update_status(self):

        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        database_handler.update_status(cursor, 1, 3)
        assert len(database_handler.query_status(cursor, 1)) == 1
        database_handler.update_status(cursor, 10, 3)
        assert len(database_handler.query_status(cursor, 11)) == 1
        database_handler.update_status(cursor, 100, 3)
        assert len(database_handler.query_status(cursor, 111)) == 1
        assert len(database_handler.query_status(cursor, 1)) == 0
        assert len(database_handler.query_status(cursor, 11)) == 0
        db.close()


class Test_database_handler_filters:

    def setup_method(self, method):
        self.db = sqlite3.connect(PATH)
        self.cursor = self.db.cursor()

        self.test_rowa = ['2015-57325012', '10/11/2015', 'Drug Incident/Investigation', 'NQ4054983', '26', '', 'Oliver Coleman',
                          '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central']

        self.test_rowb = ['2017-57325012', '10/11/2015', 'Drug Incident/Investigation', 'NQ4054983', '26', '', 'Oliver Coleman',
                          '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'task force']

        test_rowc = ['2017-57325012', '10/11/2015', 'Drug Incident/Investigation', 'NQ4054983', '26', '', 'Scott Frasier',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central']

        self.test_rowd = ['2019-57325012', '10/11/2015', 'test', 'NQ4054983', '26', '', 'Rupert Frasier',
                          '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central']

        test_many = list()
        test_many.append(self.test_rowa)
        test_many.append(self.test_rowb)
        test_many.append(test_rowc)
        test_many.append(self.test_rowd)

        database_handler.create_table(self.cursor)
        database_handler.insert_rows(self.cursor, test_many)
        self.db.commit()

    def teardown_method(self, method):
        self.db.close()
        os.remove(PATH)

    def test_remove_duplicates(self):
        assert len(database_handler.query_status(self.cursor, 0)) == 4
        database_handler.insert_rows(self.cursor, [self.test_rowa])
        assert len(database_handler.query_status(self.cursor, 0)) == 5
        self.db.commit()

    def test_check_match_case_name_arrest(self):
        # name different
        a = ['2015-57325012', '10/11/2015', 'Drug Incident/Investigation', 'NQ4054983', '26', '', 'Oliver Cole',
             '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central']
        # case-number different
        b = ['2015-5732501', '10/11/2015', 'Drug Incident/Investigation', 'NQ4054983', '26', '', 'Oliver Coleman',
             '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central']
        # arrest status different
        c = ['2015-57325012', '10/11/2015', 'Drug Incident/Investigation', 'NQ4054983', '26', 'cited', 'Oliver Coleman',
             '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central']

        assert database_handler.check_match_case_name_arrest(self.cursor, a)
        assert database_handler.check_match_case_name_arrest(self.cursor, b)
        assert database_handler.check_match_case_name_arrest(self.cursor, c)
        assert not database_handler.check_match_case_name_arrest(self.cursor, self.test_rowb)

    def test_offense_types(self):
        assert 'Drug Incident/Investigation' in database_handler.offense_types(self.cursor)
        assert 'test' in database_handler.offense_types(self.cursor)
        assert len(database_handler.offense_types(self.cursor))

    def test_filter_offenses(self):
        _test_row = [4, '2019-57325012', '10/11/2015', 'test', 'NQ4054983', '26', '', 'Rupert Frasier',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central', 0]
        _test_rowa = [4, '2019-57325012', '10/11/2015', 'NO', 'NQ4054983', '26', '', 'Rupert Frasier',
                      '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central', 0]

        assert not database_handler.filter_offenses(_test_row, set(['test']))
        assert database_handler.filter_offenses(_test_rowa, set(['test']))

    def test_filter_arrest_types(row):
        _test_row = [4, '2019-57325012', '10/11/2015', 'test', 'NQ4054983', '26', 'cited', 'Rupert Frasier',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central', 0]
        _test_rowa = [4, '2019-57325012', '10/11/2015', 'NO', 'NQ4054983', '26', '', 'Rupert Frasier',
                      '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'task force', 0]

        assert not database_handler.filter_arrest_types(_test_row)
        assert database_handler.filter_arrest_types(_test_rowa)

    def test_filter_districs(self):
        _test_row = [4, '2019-57325012', '10/11/2015', 'test', 'NQ4054983', '26', 'cited', 'Rupert Frasier',
                     '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central', 0]
        _test_rowa = [4, '2019-57325012', '10/11/2015', 'NO', 'NQ4054983', '26', '', 'Rupert Frasier',
                      '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'task force', 0]

        assert not database_handler.filter_districts(_test_row)
        assert database_handler.filter_districts(_test_rowa)


class Test_database_handler_simulate_run:

    @classmethod
    def teardown_class(cls):
        os.remove(PATH)

    def test_filter_data(self):
        db = sqlite3.connect(PATH)
        cursor = db.cursor()
        database_handler.create_table(cursor)

        test_0 = ['2015-57325012', '10/11/2015', 'valid', 'NQ4054983', '26', 'cited', 'Oliver Coleman',
                  '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central']

        test_1 = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', 'cited', 'Oliver Coleman',
                  '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central']

        test_10 = ['2015-57325012', '10/11/2015', 'valid', 'NQ4054983', '26', '', 'Oliver Coleman',
                   '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central']

        test_11 = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', '', 'Oliver Coleman',
                   '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'central']

        test_100 = ['2015-57325012', '10/11/2015', 'valid', 'NQ4054983', '26', 'cited', 'Oliver Coleman',
                    '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'invalid']

        test_101 = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', 'cited', 'Oliver Coleman',
                    '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'invalid']

        test_110 = ['2015-57325012', '10/11/2015', 'valid', 'NQ4054983', '26', '', 'Oliver Coleman',
                    '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'invalid']

        test_111 = ['2015-57325012', '10/11/2015', 'invalid', 'NQ4054983', '26', '', 'Oliver Coleman',
                    '28687 Mallard Hill', 'c66', 'Napnapan', 'CA', '10/30/1998', '63-(829)189-2968', 'White', 'Male', '', 'invalid']

        rows = [test_0, test_1, test_10, test_11, test_100, test_101, test_110, test_111]
        database_handler.insert_rows(cursor, rows)

        assert len(database_handler.query_status(cursor, 0)) == 8
        database_handler.fileter_data(cursor, ['valid'])

        assert len(database_handler.query_status(cursor, 0)) == 1
        assert len(database_handler.query_status(cursor, 1)) == 1
        assert len(database_handler.query_status(cursor, 10)) == 1
        assert len(database_handler.query_status(cursor, 11)) == 1
        assert len(database_handler.query_status(cursor, 100)) == 1
        assert len(database_handler.query_status(cursor, 101)) == 1
        assert len(database_handler.query_status(cursor, 111)) == 1
