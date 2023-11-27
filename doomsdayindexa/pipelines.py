# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import json
import os

class DoomsdayindexPipeline:
    def process_item(self, item, spider):
        return item
    


class DuplicatesPipeline:
    def open_spider(self, spider):
        if os.path.exists('doomsdata.jl') and os.path.getsize('doomsdata.jl') > 0:
            with open('doomsdata.jl', 'r') as f:
                self.urls_seen = {json.loads(line)['url'][0] for line in f}
        else:
            self.urls_seen = set()

        self.file = open("doomsdata.jl", "a")

    def process_item(self, item, spider):
        if item['url'][0] in self.urls_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.urls_seen.add(item['url'][0])
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line)
            return item

    def close_spider(self, spider):
        self.file.close()