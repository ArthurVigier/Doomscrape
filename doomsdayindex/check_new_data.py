import json
import requests
from lxml import html
from scrapy.crawler import CrawlerProcess
from doomsdayindex.spiders.doomspider import DoomspiderSpider

def check_for_new_articles(base_url, json_file): 
    response = requests.get(base_url)
    tree = html.fromstring(response.content)
    new_urls = sorted([base_url + path for path in tree.xpath('//h3/a/@href')])

    print(f"New URLs: {new_urls}")

    with open(json_file, 'r') as f:
        existing_articles = json.load(f)

    existing_urls = sorted([article['url'] for article in existing_articles])

    print(f"Existing URLs: {existing_urls}")

    # Check if all new_urls are in existing_urls
    all_urls_exist = all(url in existing_urls for url in new_urls)

    if not all_urls_exist:
        print("New articles found.")
        return True
    else:
        print("No new articles found.")
        return False
def main():
    url = 'https://thebulletin.org'
    json_file = 'doomsdayindex/doomsdayindex/doomsdata.json'
    if check_for_new_articles(url, json_file):
        process = CrawlerProcess()
        process.crawl(DoomspiderSpider)
        process.start()
    else:
        print("No new articles found.")

if __name__ == "__main__":
    main()