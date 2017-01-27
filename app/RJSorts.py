from ReadWriteExcel import ReadWriteExcel
# from app.ReadWriteExcel import ReadWriteExcel

class RJSorts:

    def __init__(self, current_path,  rows_to_check):
        self.unsorted = ReadWriteExcel(current_path)
        self.results = ReadWriteExcel()
        self.rows_to_check = rows_to_check
        sheet_list = ['north', 'south', 'east',
                      'west', 'central', 'eliminated']
        self.results.create_worksheets(sheet_list)
        self.headers = self.unsorted.copy_row(1)
        for sheet in sheet_list:
            self.results.ws = self.results.wb[sheet]
            self.results.write_row(self.unsorted.copy_row(1), bold=True)

        custody = self.unsorted.copy_col(self.headers.index('case subject custody status') + 1, 2)

        custody = self.inverse_list([''], custody)

        self.sort_dict = {'reporting district': ['north', 'south', 'east', 'west', 'central'],
                          'case subject custody status': custody,
                          'case occurred incident type': list()}

    def check_sheet(self):
        for row in self.rows_to_check:
            row_list = self.unsorted.copy_row(row)
            self.check_row(row_list)

    def check_row(self, row_list):
        results_of_check = list()
        for index, item in enumerate(row_list):
            header = self.headers[index]
            if header in self.sort_dict:
                if not self.check_cell(item, self.sort_dict[header]):
                    # excel is not zero indexed.
                    results_of_check.append(index + 1)
        self.write_sorted(row_list, results_of_check)

    def write_sorted(self, row_list, results_of_check):
        if results_of_check:
            self.results.ws = self.results.wb['eliminated']
            self.results.write_row(row_list)
            row = self.results.find_empty_row(1) - 1
            for col in results_of_check:
                self.results.highlight_cell(row, col)
        else:
            self.results.ws = self.results.wb[row_list[-1]]
            self.results.write_row(row_list)

    def inverse_list(self, exclude_list, col_list):
        # Given a list of all possible values and a list of valid values
        # return a list with only valid items.
        valid_list = [item for item in col_list if item not in exclude_list]
        
        return list(set(valid_list))

    def check_cell(self, cell_str, valid_list):
        if cell_str in valid_list:
            return True
        return False

    def save_results(self, path):
        self.results.path = path
        self.results.save_workbook()
