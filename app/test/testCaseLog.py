import os
from CaseLog import CaseLog


class TestCaseLog:

    def setup_method(self, method):
        self.log = CaseLog('{}/test_data/temp_log.xlsx'.format(os.getcwd()), test=True)
        self.log.open_or_create_index_json('{}/test_data/test_index.json'.format(os.getcwd()))

    def teardown_method(self, method):
        pass

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
