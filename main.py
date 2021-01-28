import pandas as pd


def load_data(csv_file_path):
    return pd.read_csv(csv_file_path)


if __name__ == '__main__':
    csv_file_name = 'test-data/test-data.csv'
    load_data(csv_file_name)
