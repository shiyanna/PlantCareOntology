import scrapy
import re

# Run from comand line with:
# scrapy crawl iplants -O iplants.jl

class ZakupatorSpider(scrapy.Spider):
    name = "iplants"
    
    def start_requests(self):
        urlbase = 'http://www.plantopedia.ru/encyclopaedia/pot-plant/sections.php'
        urls = [urlbase + str(n) for n in range(1,43)]
        yield scrapy.Request(url=urlbase, callback=self.parse)
        urls = [
            'https://iplants.ru/encikl.php',
            'https://iplants.ru/encikl.php?h=1',
            'https://iplants.ru/encikl.php?h=2',
            'https://iplants.ru/encikl.php?h=3',
            'https://iplants.ru/encikl.php?h=4',
            'https://iplants.ru/encikl.php?h=5',
            'https://iplants.ru/encikl.php?h=6',
            'https://iplants.ru/encikl.php?h=7',
            'https://iplants.ru/encikl.php?h=8',
            'https://iplants.ru/encikl.php?h=9',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            
        # url = 'https://iplants.ru/aucuba.htm'
        # yield scrapy.Request(url=url, callback=self.parse_plant)

    def parse(self, response):
        plant_links = response.css('.enc li a')
        yield from response.follow_all(plant_links, self.parse_plant)
        # yield response.follow(plant_links[0], callback=self.parse_plant)
            
    def parse_plant(self, response):
        re_title = re.compile('([а-яА-ЯёЁ\s\,\.]*) ([a-zA-Z\s\,\.]*) - ')
        
        header = response.css('title ::text').get()
        header_match = re_title.findall(header)
        header_ru = header_match[0][0]
        header = header_match[0][1]
        
        data = {
            'header': header ,
            'header_ru': header_ru,
        }
        
        content = response.xpath('//div[@class="content"]')[0]
        
        re_care = re.compile('.*[Уу]ход.*')
        for item in content.xpath('./h2'):
            if re_care.match(item.xpath('./text()').get()):
                blocks = item.xpath('./following::p')
                for block in blocks:
                    h = block.xpath('./em/text() | ./b/text()').getall()
                    t = block.xpath('./text()').getall()
                    h=''.join(h)
                    t=''.join(t)
                    if h!='':
                        data[h]=t
                        
                blocks = item.xpath('./following::h3')
                for block in blocks:
                    h = block.xpath('./text()').get()
                    t = block.xpath('./following::p[1]/text()').getall()   
                    t=''.join(t)
                    if h!='':
                        data[h]=t     
                    
        yield data