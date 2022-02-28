import scrapy

class ZakupatorSpider(scrapy.Spider):
    name = "zakupator"
    
    def start_requests(self):
        urlbase = 'https://zakupator.com/index/page'
        urls = [urlbase + str(n) for n in range(1,43)]
        yield scrapy.Request(url=urls[0], callback=self.parse)
        # for url in urls:
            # yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        plant_links = response.css('.ls-topic-header a')
        # yield from response.follow_all(plant_links, self.parse_plant)
        yield response.follow(plant_links[0], callback=self.parse_plant)
            
    def parse_plant(self, response):
        content_list = response.css('h2::text')
        for content in content_list:
            yield {
                'header': content.get() ,
            }