# -*- coding: utf-8 -*-
import scrapy
import json
from IDE.Tuesday.Tuesday.items import DoubanItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    # # 这里定义的设置范围是爬虫的范围
    # custom_settings = {
    #     'DEFAULT_REQUEST_HEADERS' : {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
    #     },
    # }
    # start_urls = ['http://douban.com/']
    def start_requests(self):
        page = 1
        base_url = 'https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=rank&page_limit=20&page_start={}'
        for i in range(page):
            url = base_url.format(i*1)
            yield scrapy.Request(url=url, callback=self.parse)
            # # 作用的范围是,每一个request级别
            # req = scrapy.Request(url=url, callback=self.parse)
            # req.headers['User-Agent']='Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
            # yield req

    def parse(self, response):
        json_str = response.body.decode('utf-8')
        res_dic = json.loads(json_str)
        for item in res_dic['subjects']:
            url = item['url']
            yield scrapy.Request(url=url, callback=self.parse_detailed_page)

    def parse_detailed_page(self, response):
        title = response.xpath('//h1/span[1]/text()').extract_first()
        year = response.xpath('//h1/span[2]/text()').extract_first()
        director = response.xpath('//a[@rel="v:directedBy"]/text()').extract_first()
        bianju_list = response.xpath('//div[@id="info"]/span[2]/span[@class="attrs"]/a/text()').extract()
        image = response.xpath('//img[@rel="v:image"]/@src').extract_first()

        item = DoubanItem()
        item['title'] = title
        item['year'] = year
        item['director'] = director
        item['bianju_list'] = bianju_list
        item['image'] = image
        # item['image_url'] = [image] 利用scrapy的url

        yield item




