'''
Reads the sorted excel file generated from RJSorts.py. Creates a face-sheet 
for each candidate that needs to be backgrounded. It also creates a directory 
for each Canaanite for later sharing. 

The code in this class could be reduced. I like that each section of the 
face-sheet is explicitly set. So I think here the repeated code is OK. 
'''

import os
from ReadWriteExcel import ReadWriteExcel
from FaceSheetTemplate import FaceSheetTemplate


class CreateFaceSheets:

    def __init__(self, path):
        reader = ReadWriteExcel(path)
        self.headers = reader.copy_row(1)

        out_path = os.path.dirname(path)

        if not os.path.exists(out_path + '/FaceSheets'):
            os.makedirs(out_path + '/FaceSheets')
        if not os.path.exists(out_path + '/FaceSheets/Pass'):
            os.makedirs(out_path + '/FaceSheets/Pass')
        if not os.path.exists(out_path + '/FaceSheets/Fail'):
            os.makedirs(out_path + '/FaceSheets/Fail')

        ws_list = reader.wb.get_sheet_names()
        ws_list.remove('eliminated')
        for ws in ws_list:
            reader.ws = reader.wb[ws]
            for row_index in range(2, reader.find_empty_row(1)):
                row = reader.copy_row(row_index)
                district = self.get_district(row)
                case_number = self.get_case_number(row)
                name = self.get_name(row)
                sex = self.get_sex(row)
                race = self.get_race(row)
                dob = self.get_dob(row)
                age = self.get_age(row)
                address = self.format_address(row)
                phone = self.get_phone_number(row)
                facesheet = (FaceSheetTemplate(district, case_number,
                                               name, sex, race, dob, age, address, phone))

                last_first = self.last_name_first(name)

                if not os.path.exists(out_path + '/FaceSheets/' + last_first):
                    os.makedirs(out_path + '/FaceSheets/' + last_first)

                facesheet.save_facesheet(
                    '{}/FaceSheets/{}/{}.docx'.format(out_path, last_first, last_first))

    def get_district(self, row):
        index = self.headers.index('reporting district')
        return row[index].title()

    def get_case_number(self, row):
        index = self.headers.index('case number')
        return row[index].title()

    def get_name(self, row):
        index = self.headers.index('case subject global subject')
        return row[index].title()

    def get_sex(self, row):
        index = self.headers.index('case subject global subject sex')
        return row[index].title()

    def get_race(self, row):
        index = self.headers.index('case subject global subject race')
        return row[index].title()

    def get_dob(self, row):
        index = self.headers.index(
            'case subject global subject date of birth')
        return row[index]

    def get_age(self, row):
        index = self.headers.index('case subject age')
        return row[index]

    def get_address(self, row):
        index = self.headers.index('case subject global subject address')
        return row[index].title()

    def get_address_apartment(self, row):
        index = self.headers.index(
            'case subject global subject address apartment')
        return row[index].title()

    def get_address_city(self, row):
        index = self.headers.index(
            'case subject global subject address city')
        return row[index].title()

    def get_address_state(self, row):
        index = self.headers.index(
            'case subject global subject address state')
        return row[index].upper()

    def get_phone_number(self, row):
        index = self.headers.index(
            'case subject global subject primary phone number')
        return row[index]

    def format_address(self, row):
        address_list = [self.get_address(row), self.get_address_city(row), ',',
                        self.get_address_state(row), 'APT:', self.get_address_apartment(row), ]

        return ' '.join(address_list)

    def last_name_first(self, name):
        name_list = name.split()
        name_list.insert(0, name_list.pop())
        name = "_".join(name_list)
        return name
