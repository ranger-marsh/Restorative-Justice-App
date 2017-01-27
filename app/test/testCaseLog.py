import unittest
from CaseLog import CaseLog 

'''2, 4, 12, 13, 14, 21'''

# , 'test_data/raw_test_data.xlsx'


class CaseLogTests(unittest.TestCase):

    def setUp(self):
        self.cl = CaseLog('test_data/test_case_log.xlsx')

    def tearDown(self):
        pass

    def test_create_case_list(self):
        expected = [['2015-77128059', 'william walker', 'psb', 'west'],
                    ['2015-58485596', 'megan paterson', 'psb', 'north'],
                    ['2015-76800260', 'william edmunds', 'psb', 'south'],
                    ['2015-12479434', 'rachel roberts', 'cited & released', 'north'],
                    ['2015-16531328', 'michelle bailey', 'cited & released', 'west'],
                    ['2015-57325012', 'oliver coleman', '', 'central']]

        for index, lst in enumerate(self.cl.previous_case_list):
            self.assertEqual(expected[index][0], lst[0])
            self.assertEqual(expected[index][1], lst[6])
            self.assertEqual(expected[index][2], lst[5])
            self.assertEqual(expected[index][3], lst[16])

    def test_compare_previous_current(self):

        rows_in_case_log = [2, 4, 12, 13, 14, 21]
        self.cl.compare_previous_current('test_data/raw_test_data.xlsx')
        results = self.cl.rows_to_check
        for row_index in rows_in_case_log:
            self.assertFalse(row_index in results)

if __name__ == '__main__':
    unittest.main()
