import re
import math
import random
import logging
import requests
from lxml import etree
from datetime import datetime
from bs4 import BeautifulSoup
from bs4 import NavigableString
from requests import Session
from requests.exceptions import ProxyError, RequestException


categoryTable = {
    "kitchen_display_on_website": "Kitchen & Dining",
    "pet_products_display_on_website": "Pet Supplies",
    "ce_display_on_website": "Electronics",
    "home_garden_display_on_website": "Home & Kitchen",
    "toy_display_on_website": "Toys & Games",
    "biss_display_on_website": "Health & Household",
    "health_and_beauty_display_on_website": "Health & Household",
    "home_improvement_display_on_website": "Tools & Home Improvement",
    "art_and_craft_supply_display_on_website": "Arts, Crafts & Sewing",
    "office_product_display_on_website": "Office Products",
    "13981621": "MP3 Player FM Transmitters",
    "baby_product_display_on_website": "Baby",
    "beauty_display_on_website": "Beauty & Personal Care",
    "book_display_on_website": "Books",
    "ebooks_display_on_website": "Kindle Store",
    "audible_display_on_website": "Audible Books & Originals",
    "pc_display_on_website": "Computers & Accessories",
    "lawn_and_garden_display_on_website": "Patio, Lawn & Garden",
    "1292116011": "Internal Solid State Drives",
    "595048": "External Hard Drives",
    "3015433011": "Micro SD Memory Cards",
    "1254762011": "Internal Hard Drives",
    "video_games_display_on_website": "Video Games",
    "12097479011": "Over-Ear Headphones",
    "wireless_display_on_website": "Cell Phones & Accessories",
    "525460": "Digital Picture Frames",
    "172511": "Webcams",
    "fashion_display_on_website": "Clothing, Shoes & Jewelry",
    "sports_display_on_website": "Sports & Outdoors",
    "dvd_display_on_website": "Movies & TV",
    "229189": "Computer CPU Processors",
    "10966911": "Electronics Mounts",
    "335604011": "Laptop Backpacks",
    "music_display_on_website": "CDs & Vinyl",
    "grocery_display_on_website": "Grocery & Gourmet Food"
}


def fetch_url(url, proxy="", headers={}):
    retry = 0
    while retry < 3:
        if retry > 0:
            logging.info("Retry " + str(retry))
        retry += 1
        try:
            proxy_set = {}
            if proxy is not "":
                proxy_set = {
                    "http": proxy,
                    "https": proxy,
                }
            if not headers:
                headers = {
                    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0',
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Connection": "keep-alive",
                    # "Referer": "https://www.amazon.com/",
                    "Upgrade-Insecure-Requests": "1"
                }
            if proxy_set:
                r = requests.get(url, headers=headers,
                                 proxies=proxy_set, timeout=10)
            else:
                logging.info("no proxy")
                r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 404:
                return ''
            if r.ok:
                return r.text
        except Exception as e:
            logging.warning(e)
            if proxy and retry == 3:
                return 'BLOCKED'
    return ''

def request_with_scraper_proxy(url):
    try:
        proxy = {
            "http": "http://scraperapi:d8930f592857f0335f69e7e44414100f@proxy-server.scraperapi.com:8001"
        }
        r = request("GET", url, timeout_connect=60, timeout_read=60, proxies=[proxy])
        if r.ok:
            return r.text
        else:
            return ''
    except Exception as e:
        logging.warning(e)
    return ''

def request_scraper_api(url):
    try:
        payload = {
            'api_key': 'd8930f592857f0335f69e7e44414100f', 'url': url, 'country_code': 'us'}  # , 'render': 'true'
        kwargs = {
            'params': payload
        }
        r = request("GET", url, timeout_connect=60, timeout_read=60, **kwargs)
        #r = requests.get('http://api.scraperapi.com', params=payload, timeout=60)
        if r.ok:
            return r.text
        else:
            return ''
    except Exception as e:
        logging.warning(e)
    return ''

def request(
    method, url,
    attempts=3,
    return_on_exceptions=None, return_on_status_codes=None,
    session=None,
    timeout_connect=3.05, timeout_read=3.05,
    verbose=False,
    **kwargs
):
    response = None
    _session = None
    try:
        if not return_on_exceptions:
            return_on_exceptions = []
        if not return_on_status_codes:
            return_on_status_codes = [404]
        # session
        _session = session or Session()
        # headers
        if "headers" not in kwargs:
            kwargs["headers"] = _session.headers
        # timeout
        if "timeout" not in kwargs:
            if timeout_connect or timeout_read:
                kwargs["timeout"] = (timeout_connect, timeout_read)
        # proxies
        _proxies = [None]
        proxies = kwargs.get("proxies")
        if proxies:
            if isinstance(proxies, dict):
                _proxies = [proxies]
            else:
                _proxies = proxies
        # request
        start = 1
        stop = attempts + 1
        for attempt in range(start, stop):
            kwargs["proxies"] = random.choice(_proxies)
            if verbose or attempt > 1:
                print("Attempt %s %s %s (proxies=%s)" % (attempt, method, url, kwargs["proxies"]))
            try:
                response = _session.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except RequestException as exc:
                print(exc)
                if isinstance(exc, ProxyError):
                    print("proxies = %s" % (kwargs["proxies"], ))
                if type(exc) in return_on_exceptions:
                    return response
                if response is not None and response.status_code in return_on_status_codes:
                    return response
    except Exception as exc:
        print(f"request:{exc}")
    finally:
        # close "our" session
        if not session and _session:
            _session.close()
    return response

def get_soup_from_url(url, proxy=""):
    text = request_scraper_api(url)
    if not text:
        text = fetch_url(url, proxy)
    if text == 'BLOCKED':
        return text
    elif text:
        try:
            return BeautifulSoup(text, "lxml")
        except Exception as e:
            logging.warning(e)
    return False


def get_dom_from_url(url, proxy="", isScraperRequest=True):
    if isScraperRequest:
        text = request_scraper_api(url)
        if not text:
            text = fetch_url(url, proxy)
    else:
        text = fetch_url(url, proxy)
    if text == 'BLOCKED':
        return False
    elif text:
        try:
            soup = BeautifulSoup(text, "html.parser")
            return etree.HTML(str(soup))
        except Exception as e:
            logging.warning(f"get_dom_from_url:{e}")
    return False


def list_splice(target, start, delete_count=None, *items):
    if delete_count == None:
        delete_count = len(target) - start

    # store removed range in a separate list and replace with *items
    total = start + delete_count
    removed = target[start:total]
    target[start:total] = items

    return removed

def is_blocked(ids):
    blockIds = ['px-captcha', 'sign-in-widget']
    res = list(set(ids).intersection(blockIds))
    if len(res):
        return True
    else:
        return False

def onlyNumber(text):
    res = re.findall(r'\d+', text)
    return res[0]

def extractProductId(text, disit=10):
    res = re.findall(r'\d+', text)
    for d in res:
        if len(d) == disit:
            return d
    return ''

def onlyPrice(price):
    res = price
    raw = price.replace(',', '').split("$")
    if len(raw) > 1:
        res = raw[1]
    else:
        res = raw[0]
    raw = res.split("-")
    if len(raw) > 1:
        res = raw[0].strip()
    return res


def onlyReviews(reviews):
    res = reviews.replace(' customer', '').replace(
        ' rating', '').replace('s', '').replace(',', '').strip()
    return res


def get_rank_with_category(content, res):
    content = content.split("(")[0]
    content = content.replace("#", '').replace(
        ',', '').strip()
    r = content.split(" in")
    res['rank'] = r[0].replace(' Free', '')
    if len(r) > 1:
        res['category'] = r[1].strip()
    if res['category'] == '':
        res['rank'] = ''
    return res


def get_log_value(slop, offset, sales_rank):
    log_offset = math.log10(offset)
    log_rank = math.log10(sales_rank)
    log_es = (slop * log_rank) + log_offset
    return pow(10, log_es)


def get_adjust_value(sales_rank):
    if sales_rank < 600:
        adjust = 0.3
    elif sales_rank < 800:
        adjust = 0.3
    elif sales_rank < 1000:
        adjust = 0.35
    elif sales_rank < 2000:
        adjust = 0.4
    elif sales_rank < 4000:
        adjust = 0.7
    elif sales_rank < 6000:
        adjust = 0.9
    elif sales_rank < 8000:
        adjust = 0.9
    elif sales_rank < 10000:
        adjust = 0.9
    elif sales_rank < 20000:
        adjust = 0.9
    elif sales_rank < 40000:
        adjust = 0.8
    elif sales_rank < 60000:
        adjust = 0.8
    elif sales_rank < 80000:
        adjust = 0.7
    elif sales_rank < 100000:
        adjust = 0.7
    elif sales_rank < 200000:
        adjust = 0.7
    elif sales_rank < 400000:
        adjust = 0.35
    elif sales_rank < 600000:
        adjust = 0.25
    elif sales_rank < 800000:
        adjust = 0.25
    elif sales_rank < 1000000:
        adjust = 0.15
    elif sales_rank >= 1000000:
        adjust = 0.10
    return adjust


def get_category_name(categoryId, productGroup, productTypeName):
    if productGroup == "Audible" and productTypeName == "DOWNLOADABLE_AUDIO":
        return "Audible Books & Originals"
    elif productGroup == "CE" and productTypeName == "VIDEO_GAME_HARDWARE":
        return "Electronics"
    else:
        if categoryId in categoryTable:
            return categoryTable[categoryId]
        else:
            temp = categoryId.replace("_display_on_website", "")
            temp = temp.replace("_", " ")
            temp = temp.replace("and", "&")
            return temp.title()


def get_estimated_sales(category, sales_rank):
    sales_rank = int(sales_rank)
    if not sales_rank:
        return 0
    est_sales = 0
    if category == 'Home Improvements':
        est_sales = get_log_value(-0.892647454978935,
                                  31871.6649985098, sales_rank)
        if sales_rank < 400:
            adjust = 1
            est_sales = (1 + (0.0004 * (400 - sales_rank))) * 88
        else:
            adjust = get_adjust_value(sales_rank)
        est_sales = est_sales * adjust
    elif category == "Health & Personal Care":
        est_sales = get_log_value(-1.11221344800393,
                                  402609.1695426, sales_rank)
        if sales_rank < 400:
            adjust = 1
            est_sales = (1 + (0.0004 * (400 - sales_rank))) * 158
        else:
            adjust = get_adjust_value(sales_rank)
        est_sales = est_sales * adjust
    elif category == "Clothing":
        est_sales = get_log_value(-0.890301317849426,
                                  50229.0970635419, sales_rank)
        if sales_rank < 400:
            adjust = 1
            est_sales = (1 + (0.0004 * (400 - sales_rank))) * 44
        else:
            adjust = get_adjust_value(sales_rank)
        est_sales = est_sales * adjust
    elif category == "Arts, Craft & Sewing":
        est_sales = get_log_value(-0.829766707830769,
                                  7819.72839867913, sales_rank)
        if sales_rank < 400:
            adjust = 1
            est_sales = (1 + (0.0004 * (400 - sales_rank))) * 78
        else:
            adjust = get_adjust_value(sales_rank)
        est_sales = est_sales * adjust
    elif category == "Jewelry":
        est_sales = get_log_value(-1.01346421616392,
                                  22758.7833803613, sales_rank)
        if sales_rank < 400:
            adjust = 1
            est_sales = (1 + (0.0004 * (400 - sales_rank))) * 43
        else:
            adjust = get_adjust_value(sales_rank)
        est_sales = est_sales * adjust
    elif category == "Watches":
        est_sales = get_log_value(-0.870661992348441,
                                  2130.44370633452, sales_rank)
        if sales_rank < 400:
            adjust = 1
            est_sales = (1 + (0.0004 * (400 - sales_rank))) * 72
        else:
            adjust = get_adjust_value(sales_rank)
        est_sales = est_sales * adjust
    elif category == "Music":
        est_sales = get_log_value(-0.662910080313591,
                                  738.200160843942, sales_rank)
        if sales_rank < 400:
            adjust = 1
            est_sales = (1 + (0.0004 * (400 - sales_rank))) * 45
        else:
            adjust = get_adjust_value(sales_rank)
        est_sales = est_sales * adjust
    elif category == "Movies & TV":
        est_sales = get_log_value(-1.01605292985309,
                                  33318.4010560254, sales_rank)
        if sales_rank < 400:
            adjust = 1
            est_sales = (1 + (0.0004 * (400 - sales_rank))) * 38
        else:
            adjust = get_adjust_value(sales_rank)
        est_sales = est_sales * adjust
    else:
        est_sales = get_log_value(-1.10627691729796,
                                  154077.608501638, sales_rank)
        if sales_rank < 400:
            est_sales = (1 + (0.0004 * (400 - sales_rank))) * 80
        est_sales = est_sales * 0.15
    return est_sales


def get_30days_sales(category, sales_rank):
    est_sales = get_estimated_sales(category, sales_rank)
    month = datetime.now().month
    if month == 11 or month == 12:
        est_sales = est_sales * 1
    else:
        est_sales = est_sales * 0.85
    est_sales = est_sales * 30
    est_sales = int(est_sales)
    return est_sales


def get_categories_for_fbatoolkit():
    return [
        'Toys & Games',
        'Beauty & Personal Care',
        'Health & Household',
        'Automotive',
        'Tools & Home Improvement',
        'Grocery & Gourmet Food',
        'Home & Kitchen',
        'Patio, Lawn & Garden',
        'Kitchen & Dining',
        'Sports & Outdoors',
        'Pet Supplies',
        'Arts, Crafts & Sewing',
        'Office Products',
        'Baby',
        'Cell Phones & Accessories',
        'Industrial & Scientific',
        'Electronics',
        'Musical Instruments',
        'Video Games',
        'Books',
        'Camera & Photo',
        'Computers & Accessories',
        'Amazon Launchpad',
        'Earbud & In-Ear Headphones',
        'Appliances',
        'Audio & Video Connectors & Adapters'
    ]


def get_categories_for_scout():
    return [
        'Amazon Launchpad',
        'Appliances',
        'Arts, Crafts & Sewing',
        'Automotive',
        'Baby',
        'Beauty & Personal Care',
        'Books',
        'Camera & Photo',
        'Cell Phones & Accessories',
        'Clothing, Shoes & Jewelry',
        'Collectible Coins',
        'Computers & Accessories',
        'Electronics',
        'Everything Else',
        'Grocery & Gourmet Food',
        'Health & Household',
        'Home & Kitchen',
        'Home Improvement',
        'Industrial & Scientific',
        'Jewelry',
        'Kindle Store',
        'Kitchen & Dining',
        'Musical Instruments',
        'Office Products',
        'Paid in Kindle Store',
        'Patio, Lawn & Garden',
        'Pet Supplies',
        'Shoes',
        'Software',
        'Sports & Outdoors',
        'Tools & Home Improvement',
        'Toys & Games',
        'Watches',
        'Video Games'
    ]


def generate_vid(length):
    minval = pow(10, length - 1)
    maxval = 9
    k = 1
    while k < length:
        maxval = 9 * pow(10, k) + maxval
        k += 1
    return random.randint(minval, maxval)


def generate_uid(prefix):
    return prefix + str(generate_vid(10))


def generate_utma(domainHash, visitorId, initialTime, prevSession, currentTime):
    return f"__utma={domainHash}.{visitorId}.{initialTime}.{prevSession}.{currentTime}.1"


def generate_cookies_for_fbatoolkit():
    domainHash = "182513137"
    initialTime = datetime.now().timestamp()
    initialTime = int(initialTime)
    visitorId = generate_vid(10)
    cfduid = generate_uid("dc6a3e79c1428966d3a8766f2b290e")
    utma = generate_utma(domainHash, visitorId,
                         initialTime, initialTime, initialTime)
    return f"__cfduid={cfduid}; __utmz={domainHash}.{initialTime}.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); marketchecker-check=no; __utmc={domainHash}; {utma}; __utmt=1; __utmb={domainHash}.1.10.{initialTime}"


def generate_reference_id(length):
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"
    id = []
    alphabetLength = len(alphabet) - 1
    i = 0
    while i < length:
        index = random.randint(0, alphabetLength)
        id.append(alphabet[index])
        i += 1
    return ''.join(id)


def get_cookies_for_scope():
    return 'sellerlabs_auth=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImp0aSI6IjM4MDYwN2IxYTUxNTU2NTdlYTFiNjgxMzg4M2I1YmEwMzRhMjdmMTMyNDdjMzc5Nzc1OWVmZWE1YTUyNWQ3ZDM2ODc2ZDgzZTVkYTdkNjZhIn0.eyJhdWQiOiIyIiwianRpIjoiMzgwNjA3YjFhNTE1NTY1N2VhMWI2ODEzODgzYjViYTAzNGEyN2YxMzI0N2MzNzk3NzU5ZWZlYTVhNTI1ZDdkMzY4NzZkODNlNWRhN2Q2NmEiLCJpYXQiOjE2MDI4NTA4MTQsIm5iZiI6MTYwMjg1MDgxNCwiZXhwIjoxNjM0Mzg2ODE0LCJzdWIiOiIzMzM2NyIsInNjb3BlcyI6W119.R6hU8D-jEu8bkBxFjtRJ3rzuCsqjPeyaiFfqNLUy1TLNcrpSfER0CT831WCsbHX7zaYk9WryGHeuFIyCc60-ga17aQsc9OUnczDPYcrnSu5ZbzCI28YjQedxYDyUgB2LQFvXVPGTGh6lGUsBZ2b2xHhx7_TBu77QHsMQc6Ws8u2u1rrNbtfMTpCmSVK7KaJv1kFmJsAR11Ov4ziqEPhXF0G6OVtOsdSUsX-lis3QuFoE-cx8MbZ01cfetab5htBi2WOdxtVkY-My8FcZsPRY62NJAgimf0-J0GF5XMitwUKxJ8odb1w-JSQ2aKq69611lfxmL71v-y6uxgI8GHzlNI4LE8_oj_D1AjMS_6_U6RwypyrcgTjEYGficB-Bqk-rNV-iNxX2iWaW9GB4eQaTOOhDQKmAa3c-MmB7ColcDs_XPwgaxBJnAW4iF4dYiCfNmgYzLLg0VApe1QRCbXigYHrH_Uon6agftZAQ-rZEg1s3AFqdDo8Cp1pI_1ztYppN_pumvRjp4tsRh3vjFDOsfYvQAnSFRC78pkeQTrbSWR4v2Cei9OcpGs_sq33ovWP27MwNfGiZkHUQ-AsS_Gk1evR5qxXmF3Of4a_beVMOO_UXS-NqKKubQ32wPaURC065XziIOipJGBKrWe6p-78FuWRNkrqQWGLbi0Fm3l_IO6w; sellerlabs_sso=%7B%22expires%22%3A1634386814000%7D'
