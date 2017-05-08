"""
任务过程异常
"""


class WithOutEnoughTask(Exception):
    """没有足够任务, 抛出该异常"""
    pass


class CrawlException(Exception):
    """爬虫过程异常"""
    pass
