import logging
from scripts.PageScript import PageScript
from scripts.ProdScript import ProdScript

local = True
base_path = "/home/webroisc/oaleads/"
log_path = base_path + "logs/client.log"

logging.basicConfig(filename=log_path, level=logging.INFO)  # /home/ubuntu/app/logs

def displayLog(message, type='info'):
    if local:
        print(message)
    elif type == 'info':
        logging.info(message)
    else:
        logging.warning(message)

if __name__ == '__main__':
    
    params = [{
            'tid': 0,
            'sid': 0,
            'page': 0,
            'url': "https://www.walmart.com/browse/womens-clothing/womens-pajamas-loungewear/5438_133162_5358743",
            'pagination': None,
            'xpath': "//main/div/div[3]//div[@data-item-id]/a/@href",
            'total': "//div[@data-stack-index]/div//h1/following-sibling::span[1]/text()",
            'proxyData': ['', 'http://auriza:n0t2TRpj@158.115.248.104:29842']
        }]
    for response in PageScript().request_parallel(params, size=10):
        print(response)
    params = [{
        'index': 0,
        'tid': 0,
        'sid': 3,
        'url': 'https://www.lowes.com/pd/Whirlpool-26-2-cu-ft-4-Door-French-Door-Refrigerator-with-Ice-Maker-Fingerprint-Resistant-Black-Stainless/1000332355',
        'xpaths': {
            'title': ".//div[@class='title-ivm-wrapper']/h1/text()",
            'image': ".//div[@id='main-section']/ul/li[2]//div[@class='imgContainer']/img/@src",
            'price': "//body/script[@charset='UTF-8'][1]/text():productDetails/%10/price/analyticsData/sellingPrice|//body/script[@charset='UTF-8'][1]/text():productDetails/%10/price/itemPrice",
            'upc': "//body/script[@charset='UTF-8'][1]/text():productDetails/%10/product/barcode"
        },
        'proxyData': ['', 'http://auriza:n0t2TRpj@158.115.248.104:29842']
    }]
    for response in ProdScript().request_parallel(params, size=10):
        print(response)
