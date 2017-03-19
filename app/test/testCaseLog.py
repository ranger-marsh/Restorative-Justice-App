import os
from CaseLog import CaseLog


class TestCaseLog:

    def setup_method(self, method):
        self.log = CaseLog('{}/test_data/temp_log.xlsx'.format(os.getcwd()), test=True)
        self.log.open_or_create_index_json('{}/test_data/test_index.json'.format(os.getcwd()))

    def teardown_method(self, method):
        os.remove('{}/test_data/test_index.json'.format(os.getcwd()))

    def test_create_case_list(self):
        expected = [['2015-77128059', 'william walker', 'psb', 'west'],
                    ['2015-58485596', 'megan paterson', 'psb', 'north'],
                    ['2015-76800260', 'william edmunds', 'psb', 'south'],
                    ['2015-12479434', 'rachel roberts', 'cited & released', 'north'],
                    ['2015-16531328', 'michelle bailey', 'cited & released', 'west'],
                    ['2015-57325012', 'oliver coleman', '', 'central']]

        for index, lst in enumerate(self.log.previous_case_list):
            assert expected[index][0] == lst[0]
            assert expected[index][1] == lst[6]
            assert expected[index][2] == lst[5]
            assert expected[index][3] == lst[16]

    def test_compare_previous_current(self):
        rows_in_case_log = [2, 4, 12, 13, 14, 21]
        self.log.compare_previous_current('{}/test_data/raw_test_data.xlsx'.format(os.getcwd()))
        results = self.log.rows_to_check
        for row_index in rows_in_case_log:
            assert row_index in results
            print(row_index)
        print(results)
