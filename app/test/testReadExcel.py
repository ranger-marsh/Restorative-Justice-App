import os
from ReadExcel import ReadExcel


class TestReadExcel:

    def setup_method(self, method):

        self.reader = ReadExcel('{}/test_data/raw_test_data.xlsx'.format(os.getcwd()))

    def teardown_method(self, method):
        pass

    def test_max_row_col(self):
        assert self.reader.max_row == 21
        assert self.reader.max_col == 17

    def test_clean_str(self):
        assert self.reader.clean_str(' TeSt  ') == 'test'

    def test_clean_list(self):
        dirty = ['test', '  TEST', 'TEST    ', '  tEsT  ']
        clean = ['test', 'test', 'test', 'test']
        assert self.reader.clean_list(dirty) == clean

    def test_copy_row(self):
        expected = ['case number',
                    'case occurred from date',
                    'case occurred incident type',
                    'case ori',
                    'case subject age',
                    'case subject custody status',
                    'case subject global subject',
                    'case subject global subject address',
                    'case subject global subject address apartment',
                    'case subject global subject address city',
                    'case subject global subject address state',
                    'case subject global subject date of birth',
                    'case subject global subject primary phone number',
                    'case subject global subject race',
                    'case subject global subject sex',
                    'case subject type',
                    'reporting district'
                    ]

        results = self.reader.copy_row(1)
        assert results == expected

    def test_copy_col(self):
        results = self.reader.copy_col(5, 1)
        assert results[0] == 'case subject age'
        assert results[-1] == '26'
