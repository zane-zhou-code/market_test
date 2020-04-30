# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class SinaSpider(CrawlSpider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['https://www.sina.com.cn/']

    # 全网爬取的最关键内容
    # 通过正则表达式进行判断,选择需要内容
    rules = (
        Rule(LinkExtractor(allow=r'http://sports.sina.com.cn/.*?.shtml'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        title = response.xpath('/html/head/title/text()').extract_first()
        print('获取了一个体育相关的详情页', title)
        # item = {}
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        # return item
