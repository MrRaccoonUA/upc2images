import requests
import json
import time
import logging
import re
import os
import urllib.request
from PIL import Image
from collections import namedtuple

if not os.path.exists("images"):
    os.mkdir("images")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename='log_report.txt',
                    format='%(asctime)s.%(msecs)03d[%(name)s:%(lineno)d] %(levelname)s ''%(''message)s',
                    datefmt='%Y-%m-%d %I:%M:%S')


def api_search(upc, API_URL):
    """

    :param upc: Universal Product Code
    :param API_URL: URL to which is added UPC for API request
    :return: named tuple which contains the UPC, Product Name and List of links
    """
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'user_key': 'only_for_dev_or_pro',
        'key_type': '3scale'
    }
    resp = requests.get(API_URL + upc, headers=headers)
    data = json.loads(resp.text)
    logger.info(f'UPC: {upc} - API Status: {data["code"]}')
    if data['code'] != 'OK' or len(data['items']) == 0:
        logger.error(f'UPC: {upc} - API ERROR Status: {data["code"]}')
        return None
    product_info = namedtuple('Product', 'UPC Product_Name Images_Links')
    product_info = product_info(data['items'][0]['ean'], data['items'][0]['title'], data['items'][0]['images'])
    return product_info


def link_extractor(upc, list_of_links):
    """

    :param upc: Universal Product Code
    :param list_of_links: List which contain links
    :return: named tuple with one link
    """
    def extractor(link, message):
        word = len(message)
        for item in link:
            if item[:word] == message:
                yield item

    """
    prefix: Start of the link which we need to find in the list of the links and extract all link with this start.
    https://target. - start of the Target link
    https://i5. - start of the Walmart link
    """

    def target_extractor(default_size, max_size, target):
        link = namedtuple('Link', 'resized_link')
        resized_link = re.sub(str(default_size), str(max_size), target[0])
        link = link(resized_link)
        logger.info(f'UPC: {upc} - Image Status: OK')
        return link

    def walmart_extractor(walmart):
        link = namedtuple('Link', 'resized_link')
        resized_link = re.sub(r"[?].+", "", walmart[0])
        link = link(resized_link)
        logger.info(f'UPC: {upc} - Image Status: OK')
        return link

    TARGET_DEFAULT_SIZE = 1000
    TARGET_MAX_SIZE = 3000
    prefix = 'https://target.'
    target_prefix = list(extractor(list_of_links, prefix))
    if target_prefix:
        return target_extractor(TARGET_DEFAULT_SIZE, TARGET_MAX_SIZE, target_prefix)

    prefix = 'https://i5.'
    walmart_prefix = list(extractor(list_of_links, prefix))
    if walmart_prefix:
        return walmart_extractor(walmart_prefix)

    return logger.info(f'UPC: {upc} - Image Status: No image')


def image_name(upc, product_name):
    File_Name = namedtuple('File_Name', 'name')
    character_search = re.sub(r'[-,?%/®\"]\s|(/)|(\")|[-]', ' ', product_name)
    delete_spaces = character_search.replace(' ', '_')
    delete_double_underscore = delete_spaces.replace('__', '_')
    logger.info(f'UPC: {upc} - Rename {delete_double_underscore}: OK')

    return File_Name(delete_double_underscore)


def download_image(upc, link, name, width_dimension, height_dimension):
    """

    :param upc: Universal Product Code
    :param link: url to the image
    :param name: name of the image
    :param width_dimension: specified size in width
    :param height_dimension: specified size in height
    :return: download image
    """

    def get_image_from_url(url, dir_path, full_name):
        full_path = os.path.join(dir_path, '.'.join((full_name, 'jpg')))
        urllib.request.urlretrieve(url, full_path)
        urllib.request.urlcleanup()

    im = Image.open(urllib.request.urlopen(link))
    width, height = im.size

    if width >= width_dimension or height >= height_dimension:
        get_image_from_url(link, 'images/', name)
        logger.info(f'UPC: {upc} - Download Status: OK')
    else:
        logger.error(f'UPC: {upc} - Download Status: Wrong size {width}, {height}')
    im.close()


if __name__ == '__main__':
    upc_list = []
    n = int(input("Enter number of elements: "))
    print("Enter the elements by row")

    for i in range(0, n):
        ele = int(input())
        upc_list.append(ele)
    upc_list = [str(x) for x in upc_list]

    API_URL_GET = 'https://api.upcitemdb.com/prod/trial/lookup?upc='

    for code in upc_list:

        API_COOL_DOWN_TIMEOUT_SECS = 10
        if len(upc_list) > 0 and code != upc_list[-1] and code != upc_list[0]:
            time.sleep(API_COOL_DOWN_TIMEOUT_SECS)

        detail = api_search(code, API_URL_GET)
        if not detail:
            continue
        extracted_link = link_extractor(detail.UPC, detail.Images_Links)
        if not extracted_link:
            continue
        file_name = image_name(detail.UPC, detail.Product_Name)

        WIDTH_DIMENSION, HEIGHT_DIMENSION = 600, 600

        download_image(detail.UPC, extracted_link.resized_link, file_name.name, WIDTH_DIMENSION, HEIGHT_DIMENSION)
