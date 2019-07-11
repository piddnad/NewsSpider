# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from NewsSpider.items import NewsspiderItem
import json


class NewsplusSpider(scrapy.Spider):
    '''
    通过新闻采集页面爬取
    '''

    name = 'newsplus'
    allowed_domains = ['163.com']
    start_urls = ['http://news.163.com/special/0001220O/news_json.js']

    news_list = []

    def parse(self, response):
        data = json.loads(response.text.replace("var data=", "").replace("[]]};", "[]]}"), encoding="uft-8")
        for temp_list in data["news"]:
            if len(temp_list):  # 非空
                self.news_list += temp_list

        for news in self.news_list:
            url = news['l']
            print(url)
            if 'photo' in url:
                yield scrapy.Request(url=url, callback=self.parse_photonews)
            else:
                yield scrapy.Request(url=url, callback=self.parse_news)

    def parse_news(self, response):
        item = NewsspiderItem()
        item['title'] = response.xpath("//h1/text()").extract()
        item['date'] = response.xpath("//div[@class='post_time_source']/text()").re(
            r'[0-9]*-[0-9]*-[0-9]* [0-9]*:[0-9]*:[0-9]*')
        item['source'] = response.xpath("//a[@id='ne_article_source']/text()").extract()
        # item['content'] = ''.join(response.xpath("//div[@id='endText']/p[not(@class)]").xpath('string(.)').extract())
        item['content'] = ''.join(response.xpath("//div[@id='endText']/p[not(@class)]/text()").extract()).replace('\n', '')
        item['url'] = response.url

        yield item

    def parse_photonews(self, response):
        item = NewsspiderItem()
        item['title'] = response.xpath("//h1/text()").extract()
        item['date'] = response.xpath("//div[@class='post_time_source']/text()").re(
            r'[0-9]*-[0-9]*-[0-9]* [0-9]*:[0-9]*:[0-9]*')
        item['source'] = response.xpath("//a[@id='ne_article_source']/text()").extract()
        item['content'] = ''.join(response.xpath("//div[@class='picinfo-text']/p[not(@class)]/span/text()").extract()).replace('\n', '')
        item['url'] = response.url

        yield item