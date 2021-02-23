import unittest
from main import image_name
from collections import namedtuple


class TestStringMethods(unittest.TestCase):

    def test_api_search(self):
        UPC = '820213108221'
        default_name = 'SQUARE JUICE PEACH & CARROT-25.4 FO -Pack of 8'
        File_Name = namedtuple('File_Name', 'file_name')
        expected_result = File_Name(file_name='SQUARE_JUICE_PEACH_&_CARROT_25.4_FO_Pack_of_8')
        actual_result = image_name(UPC, default_name)
        self.assertEqual(expected_result, actual_result)


if __name__ == '__main__':
    unittest.main()
