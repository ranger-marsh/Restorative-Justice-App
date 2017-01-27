import unittest
from ReadWriteExcel  import ReadWriteExcel

class ExcelReaderTests(unittest.TestCase):

    def setUp(self):
        self.reader = ReadWriteExcel('test/test_data/raw_test_data.xlsx')
        self.writer = ReadWriteExcel('test/test_data/test_write.xlsx')

    def tearDown(self):
        pass

    def test_copy_col(self):
        results = self.reader.copy_col(5, 1)
        self.assertEqual('case subject age', results[0])
        self.assertEqual('26', results[-1])

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
        self.assertEqual(expected, results)

    def test_find_empty_col(self):
        empty_col = self.reader.find_empty_col(1)
        self.assertEqual(empty_col, 18)

    def test_find_empty_row(self):
        empty_row = self.reader.find_empty_row(1)
        self.assertEqual(empty_row, 22)

    def test_max_row_col(self):
        self.assertEqual(self.reader.max_row, 21)
        self.assertEqual(self.reader.max_col, 17)

    def test_write_row(self):
        test_list = ['0', '1', '2', '3', '4', '5']
        self.writer.write_row(test_list)

        col = 1
        for list_item in test_list:
            results = self.writer.ws.cell(row=1, column=col).value
            self.assertEqual(results, list_item)
            col += 1

        test_list_b = ['0', '1', '2', '3', '4', '5', '6']
        self.writer.write_row(test_list_b)

        col = 1
        for list_item_b in test_list_b:
            results = self.writer.ws.cell(row=2, column=col).value
            self.assertEqual(results, list_item_b)
            col += 1

    def test_highlight_cell(self):
        for col in range(1, 11):
            if col % 2 == 0:
                self.writer.highlight_cell(1, col)

        for col in range(1, 11):
            if col % 2 == 0:
                self.assertIsNot(self.writer.ws.cell(
                    row=1, column=col).style.fill.start_color.index, '00000000')
            else:
                self.assertEqual(self.writer.ws.cell(
                    row=1, column=col).style.fill.start_color.index, '00000000')

    def test_build_workbook_template(self):

        ws_list = ['North', 'East', 'Central', 'South', 'West', 'Eliminated']
        headers = ['Case Number',
                   'Case Occurred From Date',
                   'Case Occurred Incident Type',
                   'Case ORI',
                   'Case Subject Age',
                   'Case Subject Custody Status',
                   'Case Subject Global Subject',
                   'Case Subject Global Subject Address',
                   'Case Subject Global Subject Address Apartment',
                   'Case Subject Global Subject Address City',
                   'Case Subject Global Subject Address State',
                   'Case Subject Global Subject Date Of Birth',
                   'Case Subject Global Subject Primary Phone Number',
                   'Case Subject Global Subject Race',
                   'Case Subject Global Subject Sex',
                   'Case Subject Type',
                   'Reporting District'
                   ]

        self.writer.create_worksheets(ws_list)

        for ws in ws_list:
            self.writer.ws = self.writer.wb[ws]
            self.writer.write_row(headers)

        self.assertListEqual(self.writer.wb.sheetnames, ws_list)

        for ws in self.writer.wb.sheetnames:
            self.writer.ws = self.writer.wb[ws]
            self.assertIsNone(self.writer.ws.cell(row=2, column=1).value)

        # if you save the file it must be deleted after every test run 
        # self.writer.save_workbook()


if __name__ == '__main__':
    unittest.main()
