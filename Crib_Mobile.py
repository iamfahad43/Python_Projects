import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CribMobileSpider(CrawlSpider):
    name = 'Crib_Mobile'
    allowed_domains = ['www.amazon.com']
    
    my_headers = {
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
    
    def start_requests(self):
        yield scrapy.Request(url='https://www.amazon.com/s?k=Crib+Mobile&crid=2D3CKP3JMCM3X&sprefix=crib+mobi%2Caps%2C419&ref=nb_sb_noss_2/', headers=self.my_headers)
        

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-3']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
    )
    
    def set_user_agent(self, request, response):
        request.headers['User-Agent'] = self.my_headers['user-agent']
        return request

    def parse_item(self, response):
        title = response.xpath("//span[@class='a-size-large product-title-word-break']/text()").get()
        title = title.strip()
        yield {
            'title': title,
        }
