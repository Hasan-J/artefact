import logging
from datetime import datetime

import scrapy
from news_websites.items import NewsArticleItem


class BbcSpider(scrapy.Spider):
    name = "bbc"
    allowed_domains = ["www.bbc.com"]

    def start_requests(self):
        url = "http://www.bbc.com/news"
        section = getattr(self, "section", None)
        if section is not None:
            url = url + "/" + section
        yield scrapy.Request(url, self.parse)

    def parse(self, response):
        """
        @url http://www.bbc.com/news
        @returns requests 40 50
        """
        yield from response.follow_all(
            response.css("a.gs-c-promo-heading[href^='/news']"), self.parse_article
        )

    def parse_article(self, response):
        """
        @url https://www.bbc.com/news/world-europe-64874255
        @returns items 1
        @scrapes body author title url crawled_at
        """
        body = response.xpath('//div[@data-component="text-block"]//text()').getall()
        author = response.css("div.ssrcss-68pt20-Text-TextContributorName::text").get()
        title = response.css("#main-heading::text").get()
        url = response.url
        crawled_at = datetime.utcnow()

        # If body contains items, then it's an article, else it's a video
        # or a sound post, which we don't want at the moment.
        if body:
            # Make sure the author item only contins the author name.
            # It could be None, some articles don't specify the author.
            if author:
                author = author.replace("By ", "")

            yield NewsArticleItem(
                body=body, author=author, title=title, url=url, crawled_at=crawled_at
            )
