#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Basic imports
from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import numpy as np
import csv
from lxml import etree
import xlwt
from xlwt import Workbook


# In[2]:


# Load Dataset
Dataset = pd.read_excel("data need to scrap.xlsx")

len(Dataset)


# In[3]:


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


# In[ ]:


# DataFrame to Scrap First 50 sku's
Test_50 = pd.DataFrame(columns=["Title", "Category1", "Category2", "Category3", "Category4", "MPN", "Verfügbar", "MOQ", "Verpackungsart", "Produktart",
                                "Artikelnummer", "EAN", "Warennummer", "Image1", "Image2"])

# Loop through the file and finding required result | Title and Category
for index, scrp_sku in enumerate(Dataset["sku"][:51]):
    url = f"https://makant-europe.de/product_info.php?products_id={scrp_sku}"
    req = requests.get(url, headers=headers)
    soup = bs4(req.content, 'lxml')
    
    # Let's find the Titles
    Title = soup.find("h3").text
    
    # Find Category
    Category1 = soup.find_all("li", {"class": "breadcrumb-item"})[0].text.strip('\r\n \t.?')      
    
    Category2 = soup.find_all("li", {"class": "breadcrumb-item"})[1].text.strip('\r\n \t.?')
    
    Category3 = soup.find_all("li", {"class": "breadcrumb-item"})[2].text.strip('\r\n \t.?')
    
    Category4 = soup.find_all("li", {"class": "breadcrumb-item"})[3].text.strip('\r\n \t.?')
    
    # First Image
    First_Image = soup.findAll("img", {"class": "img-fluid"})[0]['src']
    
    # Second Image
    Second_Image = soup.findAll("img", {"class": "img-fluid"})[1]['src']
    
    # Find Verfügbar
    Verfügbar = soup.find_all("div", {"class": "col-8 p-0 font-weight-bold text-right"})[0].text.strip('\r\n \t.?')
    
    # Find Lieferzeit:

    # Find MOQ
    MOQ = soup.find_all("div", {"class": "col-8 p-0 font-weight-bold text-right"})[1].text.strip('\r\n \t.?')
    
    # Find Verpackungsart
    Verpackungsart = soup.find_all("div", {"class": "col-8 p-0 font-weight-bold text-right"})[2].text.strip('\r\n \t.?')
    
    # Find Produktart
    Produktart = soup.find_all("div", {"class": "col-8 p-0 font-weight-bold text-right"})[3].text.strip('\r\n \t.?')
    
    # Find Artikelnummer
    Artikelnummer = soup.find_all("div", {"class": "col-8 p-0 text-right"})[0].text.strip('\r\n \t.?')
    
    # Find EAN
    EAN = soup.find_all("div", {"class": "col-8 p-0 text-right"})[1].text.strip('\r\n \t.?')
    
    # Find MPN
    MPN = soup.find_all("div", {"class": "col-8 p-0 text-right"})[2].text.strip('\r\n \t.?')
    
    # Find Warennummer
    Warennummer = soup.find_all("div", {"class": "col-8 p-0 text-right"})[3].text.strip('\r\n \t.?')
    
    
    # append in dataframe
    Test_50 = Test_50.append({'Title': Title, 'Category1': Category1, 'Category2': Category2, 'Category3': Category3, 'Category4': Category4, 'MPN': MPN,
                              'Verfügbar': Verfügbar, 'MOQ': MOQ, 'Verpackungsart': Verpackungsart,
                              'Produktart': Produktart, 'Artikelnummer': Artikelnummer, 'EAN': EAN,
                              'Warennummer': Warennummer, 'Image1': First_Image, 'Image2': Second_Image
                              }, ignore_index=True)
    


# In[ ]:


# Convert this DataFrame into Excel File

Test_50.to_excel("Web_Scraper_First50.xlsx", index=False)

