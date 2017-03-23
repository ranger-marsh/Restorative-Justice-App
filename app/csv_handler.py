"""
Open csv file with each a list. All the row-lists are contained in a list. In
preparation for entry into the database the data is cleaned. This includes not
copying the header row and lowering/stripping all the values.
"""

import csv


def open_csv(path):
    with open(path) as csvfile:
        reader = list(csv.reader(csvfile, delimiter=','))
        rows = [[val.strip().lower() for val in row] for row in reader[1:]]
    return rows


def main():
    pass

if __name__ == '__main__':
    main()
