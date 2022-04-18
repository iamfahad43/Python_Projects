#!/usr/bin/env python
# coding: utf-8

# In[44]:


# basic imports 
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

url_list = ["https://www.electrovision.co.uk/products?brand=gp+batteries%7Cduracell&cat=1185&offset=0",
            "https://www.electrovision.co.uk/products?brand=gp+batteries%7Cduracell&cat=1185&offset=12",
            "https://www.electrovision.co.uk/products?cat=1854&offset=0",
            "https://www.electrovision.co.uk/products?cat=1854&offset=12",
            "https://www.electrovision.co.uk/products?cat=1854&offset=24",
            "https://www.electrovision.co.uk/products?cat=1854&offset=36",
            "https://www.electrovision.co.uk/products?cat=1854&offset=48",
            "https://www.electrovision.co.uk/products?cat=1854&offset=60",
            "https://www.electrovision.co.uk/products?cat=1854&offset=72"]

my_df = pd.DataFrame(columns=["Title", "Product_Code", "Price", "Description", "Image_URL"])

for url in url_list:
    req = requests.get(url, headers=headers)
    soup = bs4(req.content, 'html.parser')
    
    products = soup.findAll("div", {"class": "product-thumb__content"})
    for i in products:
        # title
        TITLE = i.find("h3", {"class": "product-thumb__heading"}).text
        
        # image
        global IMAGE 
        images = i.findAll('img')
        for image in images[:1]:
            #print image source
            IMAGE = image['src']
        
        # product code
        PRODUCT_CODE = i.find("div", {"class": "product_thumb__product-code"}).text
        
        # description
        global DESCRIPTION
        for descrip in i.find("div", {"class": "product_thumb__short-desc in-list-view"}):
            DESCRIPTION = descrip.text.strip()
        
        my_df = my_df.append({"Title": TITLE, "Product_Code": PRODUCT_CODE, "Description": DESCRIPTION,
                           "Image_URL": IMAGE}, ignore_index=True)

my_df.to_excel("ElectroVision.xlsx")

