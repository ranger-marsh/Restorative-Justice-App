#!/usr/bin/env python3

"""
Open csv file with each a list. All the row-lists are contained in a list. In
preparation for entry into the database the data is cleaned. This includes
validating the headers and striping and lowering the values.
"""

import csv

HEADERS = ['case number', 'case occurred from date', 'case occurred incident type', 'case ori',
           'case subject age', 'case subject custody status', 'case subject global subject',
           'case subject global subject address', 'case subject global subject address apartment',
           'case subject global subject address city', 'case subject global subject address state',
           'case subject global subject date of birth',
           'case subject global subject primary phone number',
           'case subject global subject race', 'case subject global subject sex',
           'case subject type', 'reporting district']


def open_csv(path):
    # Open the csv file lower and strip all the values. Make sure the csv is
    # expect format.
    with open(path) as csvfile:
        reader = list(csv.reader(csvfile, delimiter=','))
        rows = [[val.strip().lower() for val in row] for row in reader]
        if rows.pop(0) != HEADERS:
            return False
    return rows


def write_receipt(path, rows):
    # Write the receipt to csv file.
    with open(f'{path}/receipt.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def main():
    pass

if __name__ == '__main__':
    main()
