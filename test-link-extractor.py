import unittest
from main import link_extractor
from collections import namedtuple


class TestStringMethods(unittest.TestCase):

    def test_api_search(self):
        UPC = '884394007308'
        Images_Links = ['https://i5.walmartimages.com/asr/20206185-284f-4e84-bba8-6243f97b65f3_1.0eeeaf4c0e89999e4ad28b38fcef5552.jpeg?odnHeight=450&odnWidth=450&odnBg=ffffff', 'https://jetimages.jetcdn.net/md5/5031713635ec2e16a5229e8d7e6bbcce.500']
        Link = namedtuple('Link', 'resized_link')
        expected_result = Link(resized_link='https://i5.walmartimages.com/asr/20206185-284f-4e84-bba8-6243f97b65f3_1.0eeeaf4c0e89999e4ad28b38fcef5552.jpeg')
        actual_result = link_extractor(UPC, Images_Links)
        self.assertEqual(actual_result, expected_result)


if __name__ == '__main__':
    unittest.main()
