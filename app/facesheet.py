'''
Takes in a list of values from the database and creates a facesheet.
'''

# import os
# from docx import Document
# from docx.enum.text import WD_ALIGN_PARAGRAPH


def assemble_address(street, apartment, city, state, zip_code):
    address = street.title()
    address += f' APT: {apartment.title()}'
    address += f' {city.title()}, '
    address += state.upper()
    address += ' ' + zip_code
    return address


def parse_row(row_list):
    info = {'case_number': row_list[1],
            'occurred_date': row_list[2],
            'incident_type': row_list[3].title(),
            'age': row_list[5],
            'name':  row_list[7].title(),
            'address': assemble_address(row_list[8], row_list[9],
                                        row_list[10], row_list[11],
                                        row_list[12],
                                        ),
            'DOB':  row_list[13],
            'phone': row_list[14],
            'race': row_list[15].title(),
            'sex': row_list[16].title(),
            'district': row_list[17].title()}
    return info


def main():
    pass


if __name__ == '__main__':
    main()
