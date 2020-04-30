# -*- coding: utf-8 -*-
import scrapy


class QimingSpider(scrapy.Spider):
    name = 'qiming'
    allowed_domains = ['5156edu.com']
    start_urls = ['http://xh.5156edu.com/xm/nu.html']

    def parse(self, response):
        # with open('mingzi.html', 'wb')as f:
        #     f.write(response.body)
        name_list = response.xpath('//a[@class="fontbox"]/text()').extract()
        two_name_list = []
        for name in name_list:
            for name2 in name_list:
                two_name = name + name2
                two_name_list.append(two_name)
        name_list = two_name_list + name_list
        # 如何在函数与函数之间传递信息
        # req,meta['wanted_name'] = last_name + name
        # post内容 scrapy.FormRequest
