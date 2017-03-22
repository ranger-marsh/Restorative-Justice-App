import read_csv
import os


def test_open_csv():
    rows = read_csv.open_csv('{}/test_data/raw_test_data.csv'.format(os.getcwd()))
    assert len(rows) == 20
    for row in rows:
        for val in row:
            assert not val.startswith(' ')
            assert not val.endswith(' ')
            if val.isalpha():
                assert val.islower()
