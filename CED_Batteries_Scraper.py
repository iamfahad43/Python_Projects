#!/usr/bin/env python
# coding: utf-8

# In[25]:


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

first_url = "https://www.ced-elec.co.uk/SearchResults/batteries"

req = requests.get(first_url, headers=headers)

soup = bs4(req.content, 'lxml')

product_list = soup.find_all("div", {"class": "CRMProdItemSummary"})

Final_Products_List = []

for index, i in enumerate(product_list):
    new_page = i.find("div", {"class": "CRMProdItemSummaryImg"})
    for link in new_page.find_all('a'):
        prd_lst = link.get('href')
        Final_Products_List.append(f"https://www.ced-elec.co.uk/SearchResults/" + prd_lst)
    
    
my_df = pd.DataFrame(columns=["Title", "Description", "Product_Code", "Price", "Image_Link"])
    
for i in Final_Products_List:
    req2 = requests.get(i, headers=headers)
    soup2 = bs4(req2.content, 'lxml')
    
    # title
    title = soup2.find("div", {"class": "v"}).text
    
    # finding images
    images = soup2.findAll('img')
    img_list = []
    for index, image in enumerate(images):
        #print image source
        img = image['src']
        img_list.append(img)
        
    global final_image
    
    for index, j in enumerate(img_list):
        if "/streamProductImage" in j:
            final_image = f"https://www.ced-elec.co.uk" + j
    
    # product code
    product_code = soup2.find("span", {"class": "v"}).text
    
    # product summary
    product_summary = soup2.find("div", {"id": "product-summary"}).text
    
    # append into dataframe
    my_df = my_df.append({"Title": title, "Description": product_summary, "Product_Code": product_code, "Image_Link": final_image}
                  ,ignore_index=True)


# In[26]:


my_df.info()


# In[27]:


my_df


# In[28]:


my_df.to_excel("CED_Electrical_Group.xlsx")


# In[ ]:




