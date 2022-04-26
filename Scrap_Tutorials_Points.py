import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ScrapTutorialsPointsSpider(CrawlSpider):
    name = 'Scrap_Tutorials_Points'
    allowed_domains = ['www.tutorialspoint.com']
    
    
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
        yield scrapy.Request(url='https://www.tutorialspoint.com/categories/development', headers=self.my_headers)
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h4[@class='h48']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="(//a[@class='page-link'])[12]"), process_request='set_user_agent'),
    )
    
    def set_user_agent(self, request, response):
        request.headers['User-Agent'] = self.my_headers['user-agent']
        return request

    def parse_item(self, response):
        title = response.xpath('//h1/text()').get()
        description = response.xpath("//div[@class='sub-title-h1']/text()").get()
        author = response.xpath("//p[@class='h24']/a/text()").get()
        author = author.strip("\xa0\xa0")
        keywords = response.xpath("//span[@class='uk-categories-list rounded']/a/text()").getall()
        language = response.xpath("//div[@class = 'course-details-info']/p[3]/text()").get()
        language = language.replace("Language -", "")
        language = language.strip("\xa0\xa0")
        publish_date = response.xpath("//div[@class = 'course-details-info']/p[4]/text()").get()
        publish_date = publish_date.strip("\xa0\xa0")
        publish_date = publish_date.replace("Published on ", "")
        
        yield {
            'title': title,
            'publish_date': publish_date,
            'language': language,
            'description': description,
            'author': author,
            'keywords': keywords,
            
        }
        
        