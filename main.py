import pandas as pd
import requests
import json
import time
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename='log_report.txt',
                    format='%(asctime)s.%(msecs)03d[%(name)s:%(lineno)d] %(levelname)s ''%(''message)s',
                    datefmt='%Y-%m-%d %I:%M:%S')


def load_data(file_path):
    return pd.read_csv(file_path, sep=",", header=None)


def api_search(list_of_upc):
    """

    :param list_of_upc: list of the UPCs that we need to lookup
    :return:
    """
    API_COOL_DOWN_TIMEOUT = 11
    df_upc_images = pd.DataFrame(data={'UPC': [], 'Product Name': [], 'Images links': []})
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'user_key': 'only_for_dev_or_pro',
        'key_type': '3scale'
    }
    for code in list_of_upc:
        start_time = datetime.now()
        resp = requests.get('https://api.upcitemdb.com/prod/trial/lookup?upc=' + code, headers=headers)
        data = json.loads(resp.text)
        time.sleep(API_COOL_DOWN_TIMEOUT)
        if data['code'] == 'OK':
            for item in data['items']:
                df_upc_images = df_upc_images.append({'UPC': item['ean'], 'Product Name': item['title'],
                                                     'Images links': item['images']}, ignore_index=True)
        logger.info(f'{list_of_upc.index(code)} UPC: {code} - Status: {data["code"]}. '
                    f'Iteration time: {datetime.now() - start_time}')
        df_upc_images['UPC'] = df_upc_images['UPC'].apply(int)
    return df_upc_images


if __name__ == '__main__':
    upc_list = []
    n = int(input("Enter number of elements: "))
    print("Enter the elements by row")
    for i in range(0, n):
        ele = int(input())
        upc_list.append(ele)

    upc_list = [str(x) for x in upc_list]
    print('Start searching...')
    df_images = api_search(upc_list)
    df_images.to_json('Report.json', orient="records")
