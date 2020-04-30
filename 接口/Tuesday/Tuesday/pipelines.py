# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
import hashlib
from scrapy.http import Request

class DoubanImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        request_list = []
        for x in item.get(self.images_urls_field, []):
            req = Request(x)
            req.meta['movie_name'] = item['title']
            request_list.append(req)
        return request_list
        # return [Request(x) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return 'full/%s.jpg' % (request.meta['movie_name'])

# 定义之后需要放到setting里面
class TuesdayPipeline(object):
    def process_item(self, item, spider):
        title = item['title']
        return item
