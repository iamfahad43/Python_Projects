# Basic imports
from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import numpy as np
import csv
from lxml import etree
import xlwt
from xlwt import Workbook
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

"""
    Going to scrap the HTML tags for description
    
"""

# Setting up the headers to avoid getting block

headers = {
    'authority': 'scrapeme.live',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}


# A URL List
url_list = ["https://cctv-direct.co.za/collections/clearance-sale", "https://cctv-direct.co.za/collections/4-camera-cctv-systems",
            "https://cctv-direct.co.za/collections/8-camera-systems", "https://cctv-direct.co.za/collections/16-32-camera-systems",
           "https://cctv-direct.co.za/collections/expandable-systems", "https://cctv-direct.co.za/collections/hikvision-turbo-hd-kits",
           "https://cctv-direct.co.za/collections/hilook-by-hikvision", "https://cctv-direct.co.za/collections/dahua-hdcvi-kits",
           "https://cctv-direct.co.za/collections/hikvision-nvrs-ip-cameras", "https://cctv-direct.co.za/collections/hikvision-cctv-cameras",
           "https://cctv-direct.co.za/collections/dvr-s", "https://cctv-direct.co.za/collections/wireless-ip-cameras",
           "https://cctv-direct.co.za/collections/hikvision-ptz-pan-tilt-zoom-cameras", "https://cctv-direct.co.za/collections/security-camera-s",
           "https://cctv-direct.co.za/collections/hikvision-ezviz-wireless-systems-cameras", "https://cctv-direct.co.za/collections/hikvision-number-plate-recognition",
            "https://cctv-direct.co.za/collections/power-supplies", "https://cctv-direct.co.za/collections/solar-panels-and-accessories",
           "https://cctv-direct.co.za/collections/led-floodlights", "https://cctv-direct.co.za/collections/accessories",
           "https://cctv-direct.co.za/collections/alarm-systems", "https://cctv-direct.co.za/collections/roboguard-askari-wireless-beams",
           "https://cctv-direct.co.za/collections/ajax-wireless-alarms-the-most-award-winning-wireless-security-system-in-europe", "https://cctv-direct.co.za/collections/car-dashcams",
           "https://cctv-direct.co.za/collections/biometric-fingerprint-readers", "https://cctv-direct.co.za/collections/led-lcd-screens",
           "https://cctv-direct.co.za/collections/intercom-systems", "https://cctv-direct.co.za/collections/inverters-batteries",
           "https://cctv-direct.co.za/collections/long-range-hikvision-ip-systems-with-ubiquiti-nanobeams", "https://cctv-direct.co.za/collections/gate-motors",
           "https://cctv-direct.co.za/collections/huawei-online-ups", "https://cctv-direct.co.za/collections/spy-gear",
           "https://cctv-direct.co.za/collections/wholesale-diy-kits"]


# DataFrame to save the results of scraped sku's
Template_DF = pd.DataFrame(columns=["DESCRIPTION"])

for base_url, scrap_url in enumerate(url_list[16:]):
    url = scrap_url
    req = requests.get(url, headers=headers)
    soup = bs4(req.content, 'lxml')
    
    product_list = []
    test = soup.find_all("div", {"class": "product span4"})
    
    for index, nest_test in enumerate(test):
        for a in nest_test.find_all("a", href=True):
            product_list.append(f"https://cctv-direct.co.za" + a['href'])
    
    for index, products in enumerate(product_list[::2]):
        new_req = requests.get(products, headers=headers)
        new_soup = bs4(new_req.content, 'lxml')

        
        Description = ""
        
        Descriptions = new_soup.findAll("div", {"class": "description"})
        
        print(f"Scraped {index+1} products from {base_url+1} url, total {len(url_list)}\n")
        Template_DF = Template_DF.append({ 
                                 "DESCRIPTION":Descriptions}
                                ,ignore_index=True)

Template_DF.to_csv('Description2.csv', sep='\t', encoding='utf-8')
Template_DF.to_excel("Description2.xlsx")
        