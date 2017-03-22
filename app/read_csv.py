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
