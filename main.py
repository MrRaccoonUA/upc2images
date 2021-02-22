import requests
import json
import time
import logging
import re
from collections import namedtuple

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename='log_report.txt',
                    format='%(asctime)s.%(msecs)03d[%(name)s:%(lineno)d] %(levelname)s ''%(''message)s',
                    datefmt='%Y-%m-%d %I:%M:%S')


def api_search(code, API_URL):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'user_key': 'only_for_dev_or_pro',
        'key_type': '3scale'
    }
    resp = requests.get(API_URL + code, headers=headers)
    data = json.loads(resp.text)
    logger.info(f'UPC: {code} - Status: {data["code"]}')
    if data['code'] != 'OK':
        return None
    product_info = namedtuple('Product', 'UPC Product_Name Images_Links')
    product_info = product_info(data['items'][0]['ean'], data['items'][0]['title'], data['items'][0]['images'])
    return product_info


def link_extractor(upc, list_of_links):
    def extractor(link, prefix):
        word = len(prefix)
        for item in link:
            if item[:word] == prefix:
                yield item

    """
    prefix: Start of the link which we need to find in the list of the links and extract all link with this start.
    https://target. - start of the Target link
    https://i5. - start of the Walmart link
    """

    def target_extractor(TARGET_DEFAULT_SIZE, TARGET_MAX_SIZE, target_prefix):
        link = namedtuple('Link', 'resized_link')
        resized_link = re.sub(str(TARGET_DEFAULT_SIZE), str(TARGET_MAX_SIZE), target_prefix[0])
        link = link(resized_link)
        logger.info(f'UPC: {upc} - Status: Image OK')
        return link

    def walmart_extractor(walmart_prefix):
        link = namedtuple('Link', 'resized_link')
        resized_link = re.sub(r"[?].+", "", walmart_prefix[0])
        link = link(resized_link)
        logger.info(f'UPC: {upc} - Status: Image OK')
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

    return logger.info(f'UPC: {upc} - Status: No image')


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
        start_time = time.time()

        detail = api_search(code, API_URL_GET)
        if not detail:
            continue
        print(type(detail.Images_Links))
        extracted_link = link_extractor(detail.UPC, detail.Images_Links)
        print(extracted_link)

        API_COOL_DOWN_TIMEOUT = 10
        iteration_time = time.time() - start_time
        cool_down = API_COOL_DOWN_TIMEOUT - iteration_time
        if len(upc_list) > 1 and code != upc_list[-1]:
            time.sleep(cool_down)
