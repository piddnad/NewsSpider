# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from NewsSpider.items import NewsspiderItem


class TechnewsSpider(CrawlSpider):
    name = 'technews'
    allowed_domains = ['163.com']
    start_urls = ['https://news.163.com',
                  'http://tech.163.com/special/gd2016/',
                  'http://tech.163.com/special/tele_2016_02/',
                  'http://tech.163.com/special/it_2016_02/',
                  'http://tech.163.com/special/internet_2016_02/',
                  'http://digi.163.com/news/',
                  'https://mobile.163.com/']

    rules = [
        Rule(
            LinkExtractor(
                allow=(
                    ('tech\.163\.com/[0-9]+/.*$'),
                    ('news\.163\.com/[0-9]+/.*$'),
                    ('digi\.163\.com/[0-9]+/.*$'),
                    ('mobile\.163\.com/[0-9]+/.*$'),
                    ('tech\.163\.com/special/gd2016.*$'),
                    ('tech\.163\.com/special/tele_2016.*$'),
                    ('tech\.163\.com/special/it_2016.*$'),
                    ('tech\.163\.com/special/internet_2016.*$'),
                    ('digi\.163\.com/special/.*$')
                ),
            ),
            callback="parse_item",
            follow=True
        )
    ]

    def parse_item(self, response):
        item = NewsspiderItem()
        if 'special' not in response.url:  # 不是新闻列表
            item['title'] = response.xpath("//h1/text()").extract()
            item['date'] = response.xpath("//div[@class='post_time_source']/text()").re(
                r'[0-9]*-[0-9]*-[0-9]* [0-9]*:[0-9]*:[0-9]*')
            item['source'] = response.xpath("//a[@id='ne_article_source']/text()").extract()
            # item['content'] = ''.join(response.xpath("//div[@id='endText']/p[not(@class)]").xpath('string(.)').extract())
            item['content'] = ''.join(response.xpath("//div[@id='endText']/p[not(@class)]/text()").extract()).replace('\n', '')
            item['url'] = response.url

        yield item

