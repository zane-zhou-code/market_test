from scrapy.cmdline import execute
import os
import sys

# 添加当前项目的绝对地址
sys.path.append(os.path.dirname(os.path.abspath('D:\Python2\IDE\Tuesday\Tuesday\main.py')))
# 执行scrapy内置的函数方法execute使用crawl爬取并调试
# execute(['scrapy', 'crawl', 'sina'])
# execute('scrapy crawl sina'.split())
# sys.path.append(os.path.dirname(os.path.abspath('D:\Python2\IDE\Tuesday\Tuesday')))
execute(["scrapy","crawl","douban"])