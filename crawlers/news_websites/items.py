# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsArticleItem(scrapy.Item):
    """Scrapy Item class that represents the news article we want to parse."""

    body = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    crawled_at = scrapy.Field()
