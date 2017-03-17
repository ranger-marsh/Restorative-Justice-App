import os
from ReadWriteExcel import ReadWriteExcel

from RJSorts import RJSorts


class TestRJSorts:

    def setup_method(self, method):
        rows_to_check = [i for i in range(2, 22)]
        self.sorts = RJSorts(
            '{}/test_data/raw_test_data.xlsx'.format(os.getcwd()), rows_to_check)

    def teardown_method(self, method):
        pass

    def test_inverse_list(self):
        col_list = ['a', 'b', 'c', 'd', 'f']
        exclude_list = ['a', 'c', 'f']
        expected = ['b', 'd']
        results = self.sorts.inverse_list(exclude_list, col_list)
        results.sort()
        assert expected == results

    def test_check_cell(self):
        valid_list = ['a', 'b', 'c']
        not_valid_list = [1, 'd', 'abc']
        for val in valid_list:
            assert self.sorts.check_cell(val, valid_list)
        for val in not_valid_list:
            assert not self.sorts.check_cell(val, valid_list)

    def test_functionally(self):
        expected = ['2015-75841199', '10/10/2015', 'theft retail', 'qi2034265', '19', 'jail', 'liam gill',
                    '155 onsgard point', 'y', 'rostock', 'oh', '10/10/1992', '977-(101)177-6436', 'white', 'male', '', 'east']

        temp = '{}/test_data/temp.xlsx'.format(os.getcwd())
        self.sorts.sort_dict['case occurred incident type'] = ['theft retail']
        self.sorts.check_sheet()
        self.sorts.save_results(temp)
        reader = ReadWriteExcel(temp)
        reader.ws = reader.wb['east']
        results = reader.copy_row(2)
        assert results == expected
        os.remove(temp)
