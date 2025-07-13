import json
import scrapy
from scrapy.crawler import CrawlerProcess
import codecs
from datetime import datetime

class TazSpider(scrapy.Spider):
    name = 'taz_spider'
    
    def __init__(self, *args, **kwargs):
        super(TazSpider, self).__init__(*args, **kwargs)
        self.updated_data = []

    def start_requests(self):
        with codecs.open('/home/taz.json', 'r', 'utf-8') as file:
            data = json.load(file)
        
        for item in data:
            url = 'https://taz.de' + item['link']
            yield scrapy.Request(url, callback=self.parse, meta={'item': item})

    def parse(self, response):
        item = response.meta['item']
        
        headline_element = response.css('span.is-flex.headline.typo-r-head-meinung-detail::text').get()
        if headline_element:
            item['headline'] = headline_element.strip()
        
        breadcrumb_text = response.css('li[data-breadcrumb-level="1"] a::text').get()
        category = breadcrumb_text.strip() if breadcrumb_text else 'undefined'
        item['category'] = category
        self.updated_data.append(item)

    def closed(self, reason):
        # Sort the updated_data list by date_time
        sorted_data = sorted(self.updated_data, key=lambda x: datetime.strptime(x['date_time'], '%Y-%m-%d %H:%M'))
        
        with codecs.open('updated_taz.json', 'w', 'utf-8') as f:
            json.dump(sorted_data, f, ensure_ascii=False, indent=4)

def run_spider():
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    })
    process.crawl(TazSpider)
    process.start()

if __name__ == '__main__':
    run_spider()