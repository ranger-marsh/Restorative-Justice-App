'''
Checks the log to see if a case has been previously checked for eligibility.
If a case appears in the log it checks to see if anything has changed. If it
has it flags it to be rechecked. 
'''

from ReadWriteExcel import ReadWriteExcel


class CaseLog:

    def __init__(self, log_path):
        self.log = ReadWriteExcel(log_path)
        self.previous_case_list = self.create_case_list(self.log)
        # rows_to_check get sent to RJSorter.py
        self.rows_to_check = list()
        self.lowest_row_index = 2

    def create_case_list(self, handler):
        # Make a list of cases from the excel file.
        row_list = list()
        for row_index in range(2, (handler.max_row + 1)):
            row_list.append(handler.copy_row(row_index))
        return row_list

    def compare_previous_current(self, current_path):
        # Make a list of row indexes that are not in the case log.
        # If any value of a row has changed since its entry into the log
        # it gets rechecked to see if in now qualifies.

        current_cases = ReadWriteExcel(current_path)
        current_case_list = self.create_case_list(current_cases)

        # If the first row of the log is empty it is new so add headers.
        if not self.previous_case_list:
            self.log.write_row(current_cases.copy_row(1), bold=True)

        rows_to_check = list()
        for index, lst in enumerate(current_case_list):
            if lst not in self.previous_case_list:
                # Adding two accounting for zero index and the header row.
                self.rows_to_check.append(index + 2)
                self.log.write_row(lst)

        if self.rows_to_check:
            self.lowest_row_index = self.rows_to_check[0]

    def save_log(self):
        self.log.save_workbook()
