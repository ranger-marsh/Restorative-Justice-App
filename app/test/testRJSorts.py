import unittest
from RJSorts import RJSorts


class TestRJSorts(unittest.TestCase):

    def setUp(self):
        rows_to_check = [i for i in range(2, 22)]
        self.sorts = RJSorts('test/test_data/raw_test_data.xlsx', rows_to_check)
       

    def tearDown(self):
        pass

    def est_functionally(self):
        # Test to see the results 
        
        self.sorts.sort_dict['case occurred incident type'] = ['theft retail']
        self.sorts.check_sheet()
        self.sorts.save_results('application/test/test_data/t_res.xlsx')

    def test_inverse_list(self):
        col_list = ['a', 'b', 'c', 'd', 'f']
        exclude_list = ['a', 'c', 'f']
        expected = ['b', 'd']
        results = self.sorts.inverse_list(exclude_list, col_list)
        results.sort()
        self.assertListEqual(expected, results)

    def test_check_cell(self):
        valid_list = ['a', 'b', 'c']
        not_valid_list = [1, 'd', 'abc']
        for val in valid_list:
            self.assertTrue(self.sorts.check_cell(val, valid_list))
        for val in not_valid_list:
            self.assertFalse(self.sorts.check_cell(val, valid_list))


if __name__ == '__main__':
    unittest.main()
