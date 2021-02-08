import unittest
from main import api_search
import pandas as pd
from pandas._testing import assert_frame_equal


class TestStringMethods(unittest.TestCase):

    def test_api_search(self):
        df = pd.read_csv('test-data/test-data.txt', sep=",", header=None)
        upc_list = []
        for el in df[0]:
            upc_list.append(el)
        upc_list = [str(x) for x in upc_list]
        expected_df_report = pd.read_json('Report.json')
        actual_df_report = api_search(upc_list)
        assert_frame_equal(actual_df_report, expected_df_report)


if __name__ == '__main__':
    unittest.main()
