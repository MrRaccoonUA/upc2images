import requests
import json
import time
import logging
import re
import os
import urllib.request
from PIL import Image
from collections import namedtuple
from tkinter.ttk import Progressbar
from tkinter import messagebox as mb

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename='log_report.txt',
                    format='%(asctime)s.%(msecs)03d[%(name)s:%(lineno)d] %(levelname)s ''%(''message)s',
                    datefmt='%Y-%m-%d %I:%M:%S')


class Downloader:
    def __init__(self, path_folder, upc, width_dimension, height_dimension, root, headers):
        self.file_path = path_folder
        upc_list = upc.split(', ')
        self.width_dimension = int(width_dimension)
        self.height_dimension = int(height_dimension)
        self.pb = Progressbar(root, orient='horizontal', mode='determinate', length=250)
        self.pb.place(relx=.1, rely=.75)
        self.pb.configure(maximum=len(upc_list))
        self.headers = headers
        if self.headers['user_key'] != 'only_for_dev_or_pro':
            self.API_URL = 'https://api.upcitemdb.com/prod/v1/lookup?upc='
            self.API_COOL_DOWN_TIMEOUT_SECS = 2
        else:
            self.API_URL = 'https://api.upcitemdb.com/prod/trial/lookup?upc='
            self.API_COOL_DOWN_TIMEOUT_SECS = 10

        for code in upc_list:
            if len(upc_list) > 0 and code != upc_list[-1] and code != upc_list[0]:
                time.sleep(self.API_COOL_DOWN_TIMEOUT_SECS)

            detail = self.api_search(code)
            if not detail:
                if code == upc_list[-1]:
                    self.pb.configure(value=upc_list.index(code) + 1)
                    self.pb.update()
                    mb.showinfo(message='The search has done!')
                continue
            extracted_link = self.link_extractor(detail.UPC, detail.Images_Links)
            if not extracted_link:
                if code == upc_list[-1]:
                    self.pb.configure(value=upc_list.index(code) + 1)
                    self.pb.update()
                    mb.showinfo(message='The search has done!')
                continue
            file_name = self.image_name(detail.UPC, detail.Product_Name)

            self.download_image(detail.UPC, extracted_link.resized_link, file_name.name)

            self.pb.configure(value=upc_list.index(code) + 1)
            self.pb.update()

            if code == upc_list[-1]:
                mb.showinfo(message='The search has done!')

    def api_search(self, upc):
        """

        :param upc: Universal Product Code
        :return: named tuple which contains the UPC, Product Name and List of links
        """
        resp = requests.get(self.API_URL + upc, headers=self.headers)
        data = json.loads(resp.text)
        logger.info(f'UPC: {upc} - API Status: {data["code"]}')
        if data['code'] != 'OK' or len(data['items']) == 0:
            logger.error(f'UPC: {upc} - API ERROR Status: {data["code"]}')
            return None
        product_info = namedtuple('Product', 'UPC Product_Name Images_Links')
        product_info = product_info(data['items'][0]['ean'], data['items'][0]['title'], data['items'][0]['images'])
        return product_info

    def link_extractor(self, upc, list_of_links):
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

    def image_name(self, upc, product_name):
        File_Name = namedtuple('File_Name', 'name')
        character_search = re.sub(r'[-,?%/®\"]\s|(/)|(\")|[-]', ' ', product_name)
        delete_spaces = character_search.replace(' ', '_')
        delete_double_underscore = delete_spaces.replace('__', '_')
        logger.info(f'UPC: {upc} - Rename {delete_double_underscore}: OK')

        return File_Name(delete_double_underscore)

    def download_image(self, upc, link, name):
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

        if width >= self.width_dimension or height >= self.height_dimension:
            get_image_from_url(link, self.file_path + '/',  name)
            logger.info(f'UPC: {upc} - Download Status: OK')
        else:
            logger.error(f'UPC: {upc} - Download Status: Wrong size {width}, {height}')
        im.close()
