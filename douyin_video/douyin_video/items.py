# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DouyinVideoItem(scrapy.Item):
    video_title = scrapy.Field()
    video_url = scrapy.Field()
    video_id = scrapy.Field()

