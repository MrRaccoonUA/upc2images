import unittest
from main import api_search
from collections import namedtuple


class TestStringMethods(unittest.TestCase):

    def test_api_search(self):
        code = '884394007308'
        Product = namedtuple('Product', 'UPC Product_Name Images_Links')
        expected_result = Product(UPC='0884394007308', Product_Name='OKF Farmers Aloe Drink, Original, 50.7 Fl Oz', Images_Links=['https://i5.walmartimages.com/asr/20206185-284f-4e84-bba8-6243f97b65f3_1.0eeeaf4c0e89999e4ad28b38fcef5552.jpeg?odnHeight=450&odnWidth=450&odnBg=ffffff', 'https://jetimages.jetcdn.net/md5/5031713635ec2e16a5229e8d7e6bbcce.500'])
        actual_result = api_search(code, API_URL='https://api.upcitemdb.com/prod/trial/lookup?upc=')
        self.assertEqual(actual_result, expected_result)


if __name__ == '__main__':
    unittest.main()
