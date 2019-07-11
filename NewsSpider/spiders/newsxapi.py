# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from NewsSpider.items import NewsspiderItem
import json


class NewsxApiSpider(scrapy.Spider):
    '''
    通过新闻获取API爬取
    '''

    name = 'newsxapi'
    allowed_domains = ['163.com']
    # start_urls = ['http://news.163.com/special/0001220O/news_json.js']

    start_news_category = ["guonei", "guoji", "yaowen", "shehui", "war", "money",
                           "tech", "sports", "ent", "auto", "jiaoyu", "jiankang", "hangkong"]
    news_url_head = "http://temp.163.com/special/00804KVA/"
    news_url_tail = ".js?callback=data_callback"

    def start_requests(self):
        for category in self.start_news_category:
            category_item = "cm_" + category
            for count in range(1, 20):  # 每个版块最多爬取前20页数据
                if count == 1:
                    start_url = self.news_url_head + category_item + self.news_url_tail
                else:
                    start_url = self.news_url_head + category_item + "_0" + self.news_url_tail
                yield scrapy.Request(start_url, meta={"category": category}, callback=self.parse_news_list)

    def parse_news_list(self, response):
        # 爬取每个url
        json_array = "".join(response.text[14:-1].split())  # 去掉前面的"data_callback"
        news_array = json.loads(json_array)
        category = response.meta['category']
        for row in enumerate(news_array):
            news_item = NewsspiderItem()
            row_data = row[1]
            news_item["url"] = row_data["tlink"]

            yield scrapy.Request(news_item["url"], meta={"news_item": news_item},
                                 callback=self.parse_news_content)

    def parse_news_content(self, response):
        source = "//a[@id='ne_article_source']/text()"
        content_path = "//div[@id='endText']/p/text()"

        content_list = []
        for data_row in response.xpath(content_path).extract():
            content_list.append("".join(data_row.split()))
        content_list = "\"".join(content_list)
        news_item = response.meta['news_item']
        news_item["content"] = content_list
        news_item["source"] = response.xpath(source).extract_first()
        news_item['title'] = response.xpath("//h1/text()").extract()
        news_item['date'] = response.xpath("//div[@class='post_time_source']/text()").re(
            r'[0-9]*-[0-9]*-[0-9]* [0-9]*:[0-9]*:[0-9]*')

        yield news_item
