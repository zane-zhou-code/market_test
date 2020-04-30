# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
# 引入scrapy内部的元素,需要使用的是项目文件夹内的文件开始
from IDE.Tuesday.Tuesday.items import LianjiaLItem

class LianjiaSpider(scrapy.Spider):
    # 指定的名字
    name = 'lianjia'
    # 合法的域名
    allowed_domains = ['lianjia.com']
    # 起始地址
    start_urls = ['https://jx.lianjia.com/zufang/rs/']

    # 默认的对应函数
    # 这里的response与requests.get返回值response不是同一个东西
    def parse(self, response):
        with open('lianjia.html', 'wb')as f:
            # 使用 body 来获取二进制返回值信息
            f.write(response.body)

        # 通过XPATH获取具体内容
        hrefs  = response.xpath('//p[@class="content__list--item--title twoline"]/a/@href').extract()
        print(hrefs)
        #循环访问每个详情页的信息
        for href in hrefs:
            href = response.urljoin(href)# 等同href = parse.urljoin(response.url, href)
            req = scrapy.Request(url=href, callback=self.parse_detailed_page)
            yield req

    def parse_detailed_page(self, response):
        title = response.xpath('//p[@class="content__title"]/text()').extract_first  # 或者extract()[0]列表第0个
        print(title)
        # 生成items
        item = LianjiaLItem
        # 对于items的对象,只能使用字典的方式访问
        item['title'] = title

        yield item

