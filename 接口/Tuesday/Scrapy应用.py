
# Scheduler:调度器,主要功能是将Request(URL-函数)存储在这之中
# Downloader:下载器,获取html信息
# Spiders:爬虫程序
# Item Pipeline:内容管道
# Scrapy Engine:支持多线程
# scrapy startproject Tuesday
# scrapy genspider lianjia lianjia.com 创建爬虫
# scrapy crawl lianjia 执行爬虫
# scrapy shell 网址
#              print(response.body.decode('utf-8')
# scrapy genspider -t crawl sina sina.com 全局爬取
# 分布式 redits




# 1.初始的时候,我们需要添加start_url 或者是实现start_requests函数
# 就会生成初始的Request,初始Request会被发送到Engine中,不会经过Spiders中间件

# 2.Engine会将Requests放置到Scheduler中存储,等待Enigine获取并下载内容

# 3.Engine会根据当前的并发数量选择获取Scheduler中的Request下载,CONCURRENT_REQUESTS

# 4.Engine获取Request之后,会调用downloader下载池,在这个过程中,会经过Downloader中间件
# process_request()

# 5.Downloader 下载Request对应的内容 Response,之后会返回给Engine,会经过Downloader中间件
# process_response()

# 6.将Response返回给Spiders,这之中会经过Spiders中间价,process_spider_input()

# 7.Spider处理Response获取Items或者是Request,返回给Engine,这之中会经过Spiders中间价,process_spider_output()

# 8.Enigine会区分获取的是Items还是Requests,如果是Items发送给Item Pipeline,如果是Request,发送给Scheduler

# 9。循环第三步