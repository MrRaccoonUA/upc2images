import pytest
import os
from collections import namedtuple
from main import api_search, link_extractor, image_name, download_image


class TestClass:
    Product = namedtuple('Product', 'UPC Product_Name Images_Links')

    @pytest.mark.parametrize('upc, expect_result', [('884394007308', Product(UPC='0884394007308',
                                                                             Product_Name='OKF Farmers Aloe Drink, Original, 50.7 Fl Oz',
                                                                             Images_Links=[
                                                                                 'https://i5.walmartimages.com/asr/20206185-284f-4e84-bba8-6243f97b65f3_1.0eeeaf4c0e89999e4ad28b38fcef5552.jpeg?odnHeight=450&odnWidth=450&odnBg=ffffff',
                                                                                 'https://jetimages.jetcdn.net/md5/5031713635ec2e16a5229e8d7e6bbcce.500'])),
                                                    ('820213108221', Product(UPC='0820213108221',
                                                                             Product_Name='SQUARE JUICE PEACH & CARROT-25.4 FO -Pack of 8',
                                                                             Images_Links=[
                                                                                 'http://site.unbeatablesale.com/EB139/kehe24979.gif'])),
                                                    ('47100000527', None),
                                                    ('754177830518',
                                                     Product(UPC='0754177830518', Product_Name='DRINK MIX',
                                                             Images_Links=[
                                                                 'https://i5.walmartimages.com/asr/231f47be-5980-439f-b719-268610c00a11_4.eb53f23061184bc21a730dc14ab350f0.png?odnHeight=450&odnWidth=450&odnBg=ffffff',
                                                                 'http://www.meijer.com/assets/product_images/styles/xlarge/1003855_233259_A_400.jpg',
                                                                 'http://site.unbeatablesale.com/img684/kehe31225.gif',
                                                                 'http://8016235491c6828f9cae-6b0d87410f7cc1525cc32b79408788c4.r96.cf2.rackcdn.com/1705/58803953_1.jpg',
                                                                 'http://images.jet.com/md5/41538fdfa265f614b7825a81a5d0f95d.500',
                                                                 'https://d29pz51ispcyrv.cloudfront.net/images/I/x5unua0kkGXgR9Qxm.MD256.JPEG']))])
    def test_api_search(self, upc, expect_result):
        actual_result = api_search(upc, 'https://api.upcitemdb.com/prod/trial/lookup?upc=')
        assert actual_result == expect_result

    Link = namedtuple('Link', 'resized_link')

    @pytest.mark.parametrize('upc, Images_Links, expect_result', [('0884394007308', [
        'https://i5.walmartimages.com/asr/20206185-284f-4e84-bba8-6243f97b65f3_1.0eeeaf4c0e89999e4ad28b38fcef5552.jpeg?odnHeight=450&odnWidth=450&odnBg=ffffff',
        'https://jetimages.jetcdn.net/md5/5031713635ec2e16a5229e8d7e6bbcce.500'], Link(
        resized_link='https://i5.walmartimages.com/asr/20206185-284f-4e84-bba8-6243f97b65f3_1.0eeeaf4c0e89999e4ad28b38fcef5552.jpeg')),
                                                                  ('820213108221', [
                                                                      'http://site.unbeatablesale.com/EB139/kehe24979.gif'],
                                                                   None),
                                                                  ('754177830518', [
                                                                      'https://i5.walmartimages.com/asr/231f47be-5980-439f-b719-268610c00a11_4.eb53f23061184bc21a730dc14ab350f0.png?odnHeight=450&odnWidth=450&odnBg=ffffff',
                                                                      'http://www.meijer.com/assets/product_images/styles/xlarge/1003855_233259_A_400.jpg',
                                                                      'http://site.unbeatablesale.com/img684/kehe31225.gif',
                                                                      'http://8016235491c6828f9cae-6b0d87410f7cc1525cc32b79408788c4.r96.cf2.rackcdn.com/1705/58803953_1.jpg',
                                                                      'http://images.jet.com/md5/41538fdfa265f614b7825a81a5d0f95d.500',
                                                                      'https://d29pz51ispcyrv.cloudfront.net/images/I/x5unua0kkGXgR9Qxm.MD256.JPEG'],
                                                                   Link(
                                                                       resized_link='https://i5.walmartimages.com/asr/231f47be-5980-439f-b719-268610c00a11_4.eb53f23061184bc21a730dc14ab350f0.png'))])
    def test_link_extractor(self, upc, expect_result, Images_Links):
        link_actual_result = link_extractor(upc, Images_Links)
        assert link_actual_result == expect_result

    File_Name = namedtuple('File_Name', 'name')

    @pytest.mark.parametrize('upc, default_name, expect_result', [('0884394007308',
                                                                   'OKF Farmers Aloe Drink, Original, 50.7 Fl Oz',
                                                                   File_Name(
                                                                       name='OKF_Farmers_Aloe_Drink_Original_50.7_Fl_Oz')),
                                                                  ('754177830518', 'DRINK MIX',
                                                                   File_Name(name='DRINK_MIX'))])
    def test_image_name(self, upc, default_name, expect_result):
        name_actual_result = image_name(upc, default_name)
        assert name_actual_result == expect_result

    @pytest.mark.parametrize('upc, resized_link, name', [('0884394007308',
                                                          'https://i5.walmartimages.com/asr/20206185-284f-4e84-bba8-6243f97b65f3_1.0eeeaf4c0e89999e4ad28b38fcef5552.jpeg',
                                                          'OKF_Farmers_Aloe_Drink_Original_50.7_Fl_Oz'),
                                                         ('754177830518',
                                                          'https://i5.walmartimages.com/asr/231f47be-5980-439f-b719-268610c00a11_4.eb53f23061184bc21a730dc14ab350f0.png',
                                                          'DRINK_MIX')])
    def test_download_image(self, upc, resized_link, name):
        WIDTH_DIMENSION, HEIGHT_DIMENSION = 600, 600
        download_image(upc, resized_link, name, WIDTH_DIMENSION, HEIGHT_DIMENSION)
        assert os.path.isfile('images/' + name + '.jpg')
