# Scrapy settings for example project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
SPIDER_MODULES = ['JD.spiders']
NEWSPIDER_MODULE = 'JD.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'

# 设置重复过滤器的模块
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# 设置调度器 具备与数据库交互的功能
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# 当爬虫结束的时候是否保存数据库数据
SCHEDULER_PERSIST = True
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
#SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"

ITEM_PIPELINES = {
    # 'example.pipelines.ExamplePipeline': 300,
    # 开启该管道，会自动把数据保存在redis数据库中
    'scrapy_redis.pipelines.RedisPipeline': 400,
}
# 设置redis数据库
REDIS_URL = "redis://python:snackdeng@127.0.0.1:6379"

# LOG_LEVEL = 'DEBUG'

# Introduce an artifical delay to make use of parallelism. to speed up the
# crawl.

DOWNLOAD_DELAY = 1
