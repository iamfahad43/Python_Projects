import scrapy
import logging

class ToturialspointSpider(scrapy.Spider):
    name = 'Toturialspoint'
    allowed_domains = ['www.tutorialspoint.com']
    start_urls = ['https://www.tutorialspoint.com/categories/development?page=1']

    def parse(self, response):
        
        links = response.xpath("//h4/a")
       
        for link in links:
        
            nes_link = link.xpath(".//@href").get()
           
            yield scrapy.Request(url=nes_link, callback=self.course_link)
           #yield response.follow(url=nes_link, callback=self.course_link)

            next_page_link = response.xpath("//a[@class='page-link']/@href").get()
                
            if next_page_link:
                yield scrapy.Request(url=next_page_link, callback=self.parse)
        
            
           
           
    def course_link(self, response):
        title = response.xpath("//h1/text()").get()
        description = response.xpath("//div[@class='sub-title-h1']/text()").get()
        author = response.xpath("//p[@class='h24']/a/text()").get()
        author = author.strip("\xa0\xa0")
        keywords = response.xpath("//span[@class='uk-categories-list rounded']/a/text()").getall()
        language = response.xpath("//div[@class = 'course-details-info']/p[3]/text()").get()
        #language = language.strip("\xa0$0")
        language = language.replace("Language -", "")
        
        publish_date = response.xpath("//div[@class = 'course-details-info']/p[4]/text()").get()
        publish_date = publish_date.strip("\xa0\xa0")
        publish_date = publish_date.replace("Published on ", "")
        
        yield {
            'title': title,
            'discription': description,
            'author': author,
            'keywords': keywords,
            'language': language,
            'publish_date': publish_date
            }
        
    
        