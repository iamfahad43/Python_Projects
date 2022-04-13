#import re
import sys
#import xmltodict
import json
#import time
#import mws
import base64
import logging
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from requests.utils import requote_uri
from utilities import ScriptHelper

proxy_stores = [3, 4, 7]

class ProdScript():
    def get_est_sales_from_scout(self, rank, category):
        category = requote_uri(category).replace('&', '%26')
        url = f"https://amzscout.net/api/v1/landing/sales?domain=COM&category={category}&rank={rank}"
        response = ScriptHelper.fetch_url(url)
        response = json.loads(response)
        if "sales" in response:
            return response['sales']
        return 0

    def get_est_sales_from_fbatoolkit(self, data):
        # print("Request to estimated sales")
        logging.info("Request to estimated sales")
        cookies = ScriptHelper.generate_cookies_for_fbatoolkit()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Referer': 'https://fbatoolkit.com/',
            'Cookie': cookies
        }
        category_bytes = data['category'].encode('ascii')
        base64_bytes = base64.b64encode(category_bytes)
        base64_category = base64_bytes.decode('ascii')
        url = "https://fbatoolkit.com/estimate_ajax?category=" + \
            base64_category + "&rank=" + data['rank']
        response = ScriptHelper.fetch_url(url, "", headers)
        if "sales_per_day_30day_avg" in response:
            result = json.loads(response)
            if result['sales_per_day_30day_avg']:
                avg_sales = result['sales_per_day_30day_avg'].replace(
                    "More than ", "").replace("Less than ", "")
                if "every" in avg_sales:
                    avg_sales = 1
                data['sales'] = int(avg_sales) * 30
                if not data['price']:
                    data['revenue'] = 0
                else:
                    data['revenue'] = round(
                        data['sales'] * float(data['price']), 2)
        return data

    def get_est_sales(self, data):
        fbaCategories = ScriptHelper.get_categories_for_fbatoolkit()
        if data['category'] in fbaCategories:
            data = self.get_est_sales_from_fbatoolkit(data)
        else:
            scoutCategories = ScriptHelper.get_categories_for_scout()
            if data['category'] in scoutCategories:
                est_sales = self.get_est_sales_from_scout(
                    data['rank'], data['category'])
            else:
                est_sales = ScriptHelper.get_30days_sales(
                    data['category'], int(data['rank']))
            data['sales'] = est_sales
            data['revenue'] = round(est_sales * float(data['price']))
        return data
    '''
    def get_amz_product_info_from_api(self, data, account):
        res = []
        try:
            api = mws.Products(account['access_key'], account['secret_key'],
                               account['merchant_id'], auth_token=account['auth_token'])
            ids = [x.get('asin') for x in data]
            result = api.get_matching_product_for_id(
                marketplaceid="ATVPDKIKX0DER",
                type_="ASIN",
                ids=ids,
            )
            for index, item in enumerate(result.parsed):
                if item['status'] == 'Success':
                    product = item['Products']['Product']
                    info = {'rank': '', 'category': '',
                            'revenue': '0', 'sales': '0'}
                    itemAttributes = product['AttributeSets']['ItemAttributes']
                    info['title'] = itemAttributes['Title']
                    info['price'] = data[index]['price']
                    info['reviews'] = data[index]['reviews']
                    productGroup = itemAttributes['ProductGroup']
                    productTypeName = itemAttributes['ProductTypeName']
                    if product['SalesRankings'] and len(product['SalesRankings']['SalesRank']):
                        rankData = product['SalesRankings']['SalesRank'][0]
                        info['category'] = ScriptHelper.get_category_name(
                            rankData['ProductCategoryId'], productGroup, productTypeName)
                        info['rank'] = rankData['Rank']
                        if info['rank']:
                            info = self.get_est_sales(info)
                    res.append({'asin': data[index]['asin'], 'info': info})
        except Exception as ex:
            err = xmltodict.parse(ex.args[0])
            errCode = err['ErrorResponse']['Error']['Code']
            # if errCode == 'RequestThrottled':
            # time.sleep(1)
            # self.get_product_info_from_api(data, account)
        return res
    '''

    def get_item_field(self, dom, xpath, url='', content=None):
        try:
            if ':' in xpath and not 'price:' in xpath:
                temps = xpath.split("|")
                for temp in temps:
                    splits = temp.split(":")
                    xpath = splits[0]
                    keys = splits[1].split("/")
                    if content is None:
                        data = dom.xpath(xpath)
                        if data:
                            content = data[0].replace("window['__PRELOADED_STATE__'] = ", "")
                            if "__APOLLO_STATE__" in content:
                                content = content.replace("window.__APOLLO_STATE__=", "").strip()
                                content = content[:-1]
                            if "__PRELOADED_STATE__" in content:
                                content = content.replace("window.__PRELOADED_STATE__ = ", "")
                    if content is not None:
                        tempjson = json.loads(content.strip())
                        isValidkeys = True
                        for key in keys:
                            if '%' in key:
                                keySplits = key.split('%')
                                if keySplits[1]:
                                    keySplits[1] = ScriptHelper.extractProductId(url, int(keySplits[1]))
                                    key = "".join(keySplits)
                                else:
                                    key = keySplits[0]
                                    for k in tempjson.keys():
                                        if key in k:
                                            key = k
                            elif key.isnumeric() and type(tempjson) is list:
                                tempjson = tempjson[int(key)]
                                continue
                            if dom is None and tempjson:
                                print(key, tempjson.keys())
                            if tempjson and key in tempjson:
                                tempjson = tempjson[key]
                            else:
                                isValidkeys = False
                                break
                        if isValidkeys:
                            return tempjson
            else:
                res = dom.xpath(xpath)
                if res:
                    return res[0]
        except Exception as ex:
            print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), type(ex).__name__, ex)
        return ''
    
    def get_price_for_lowes(self, url, xpath):
        productId = ScriptHelper.extractProductId(url)
        response = ScriptHelper.request_with_scraper_proxy(f"https://www.lowes.com/pd/{productId}/productdetail/1555/Guest")
        print(response)
        if response:
            return self.get_item_field(None, xpath, url, response)
        return ''    

    def get_product_info(self, params):
        res = {'error': True, 'found': False}
        dom = ScriptHelper.get_dom_from_url(params['url'], params['proxyData'][1], False if params['sid'] in proxy_stores else True)
        if type(dom) is not bool and dom is not None:
            res['error'] = False
            xpaths = params['xpaths']
            upc = self.get_item_field(dom, xpaths['upc'], params['url'])
            if upc:
                res['found'] = True
                res['info'] = {
                    'upc': upc,
                    'link': params['url'],
                    'title': self.get_item_field(dom, xpaths['title'], params['url']),
                    'image': self.get_item_field(dom, xpaths['image'], params['url']),
                    'price': 0
                }
                price = self.get_item_field(dom, xpaths['price'], params['url'])
                if price:
                    res['info']['price'] = ScriptHelper.onlyPrice(str(price))
        return res

    def script_handler(self, params):
        res = self.get_product_info(params)
        res['tid'] = params['tid']
        res['sid'] = params['sid']
        return res

    def request_parallel(self, payloads, size=1):
        items_len = len(payloads)
        max_workers = min(items_len, size)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.script_handler, item) for item in payloads}
            completed_futures = concurrent.futures.as_completed(futures)
            for n, future in enumerate(completed_futures, 1):
                yield future.result()
