import json

import scrapy
from scrapy.loader import ItemLoader

from vietnambusinessinsider.items import VietnambusinessinsiderItem


class VnbiSpider(scrapy.Spider):
    name = "vnbi"
    url = 'https://vietnambusinessinsider.vn/recent-post?limit=10&page={}&not_in_ids=&not_in_block=1&not_in_cate_ids='
    start_urls = ['https://vietnambusinessinsider.vn/recent-post?limit=5&block_id=1', url.format(1)]

    def parse(self, response):
        data = json.loads(response.text)

        for post in data['data']:
            il = ItemLoader(item=VietnambusinessinsiderItem(), selector=post)
            date_time = post['published_at'].split()

            il.add_value('ID', post['id'])
            il.add_value('author', post['author'])
            il.add_value('author_url', post['author_url'])
            il.add_value('title', post['name'])
            il.add_value('date_post', date_time[0])
            il.add_value('time_post', date_time[1])
            il.add_value('link', post['link'])
            yield il.load_item()

        try:
            has_next = data['meta']['pagination']['links']['next']
        except KeyError:
            has_next = None

        if has_next is not None:
            next_page = data['meta']['pagination']['current_page'] + 1
            yield scrapy.Request(url=self.url.format(next_page), callback=self.parse)
