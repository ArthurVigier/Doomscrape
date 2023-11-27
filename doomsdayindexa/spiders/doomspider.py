import scrapy
from doomsdayindexa.items import DoomItem
import random

class DoomspiderSpider(scrapy.Spider):
    name = "doomspider"
    allowed_domains = ["thebulletin.org"]
    start_urls = ["https://thebulletin.org"]

    custom_settings = {
        "FEEDS": {
            "doomsdata.json": {"format": "json", 'overwrite': True},
        }
    }

    def parse(self, response):
        entries = response.css('h3')
        for entrie in entries:
            relative_url = entrie.css('h3 a ::attr(href)').get()

            if 'premium/' in relative_url:
                entrie_url = 'https://thebulletin.org/' + relative_url
            else:
                entrie_url = 'https://thebulletin.org/' + relative_url
            yield response.follow(entrie_url, callback=self.parse_doom_page)

    def parse_doom_page(self, response):
                doom_item = DoomItem()
        
                doom_item['url'] = response.url,
                doom_item['title'] = response.xpath('//meta[@property="og:title"]/@content').get()
                doom_item['paragraph'] = response.css('.fl-html p::text').get(),
                doom_item['published_time'] = response.xpath('//meta[@property="article:published_time"]/@content').get()
        
                yield doom_item
            
       
