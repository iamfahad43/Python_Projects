import scrapy
import json

class ScrapQuotesSpider(scrapy.Spider):
    name = 'scrap_quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):
        # load the response data into json
        response_body = json.loads(response.body)
        # fetching quotes from that site
        quotes = response_body.get('quotes')
        
        for quote in quotes:
            # get the auther name 
            author = quote.get('author').get('name')
            # get the tags
            tags = quote.get('tags')
            # get the text content
            text_content = quote.get('text')
            
            # here what we will show in decorators
            yield {
                'author': author,
                'tags': tags,
                'text_content': text_content
            }
            
        
        # let's find the last page and request it agin to fetch all the quotes from that site
        has_next_page = response_body.get('has_next')
        if has_next_page:
            next_page_number = response_body.get('page') + 1
            yield scrapy.Request(url=f"https://quotes.toscrape.com/api/quotes?page={next_page_number}", callback=self.parse)
        
