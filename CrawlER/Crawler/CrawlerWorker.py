"""爬虫工作者, 接收请求参数进行爬虫
"""
import time
import requests

from CrawlER.CrawlUtils.CrawlRequest import crawl_file, crawl_html, parse_file, parse_html
from CrawlER.Exception import WithOutEnoughTask, CrawlException


class CrawlerWorker(object):
    """爬虫worker

    Attributes:
        task_manager: 任务管理器
        headers_manager: 请求头管理器

        max_crawl_num: 最大爬虫次数
        __current_headers: 当前的请求头
        __session: 当前请求会话

    Methods:
        crawl: 爬虫请求
        crawl_repeatedly: 爬虫请求计划
        start: 开始workers任务

        __reset_current_headers: 设置当前请求头
    """
    def __init__(self, task_manager, headers_manager=None, max_crawl_num=100):
        self.task_manager = task_manager
        self.headers_manager = headers_manager

        self.max_crawl_num = max_crawl_num

        self.__session = None
        self.__current_headers = None

    def crawl(self):
        """爬虫请求"""
        # 获取请求任务, 确认请求的类型
        crawl_task = self.task_manager.get_task()
        crawl_func = crawl_html if not crawl_task.crawl_file else crawl_file

        # 获取请求, 解析结果
        res = crawl_func(self.session, crawl_task.request_url, crawl_task.timeout,
                         **{"headers": self.__current_headers})
        soup = parse_html(res.content)

        # 解析数据
        try:
            crawl_task.func(res, soup, **crawl_task.other)
        except Exception as e:
            crawl_task.record_error(e)
            raise CrawlException(e)

        # 间隔爬虫
        time.sleep(crawl_task.spacing_time)

    def crawl_repeatedly(self):
        """多次爬虫请求"""
        for i in range(self.max_crawl_num):
            try:
                self.crawl()
            except WithOutEnoughTask as e:
                raise WithOutEnoughTask("没有足够任务参数")
            except CrawlException:
                break

        # 重新设置会话, 请求头, 代理
        self.__reset_current_headers()
        self.__reset_current_session()

    def start(self):
        """开始爬虫worker任务"""
        while True:
            try:
                self.crawl_repeatedly()
            except WithOutEnoughTask:
                print("没有足够任务")
                break

    def __reset_current_session(self):
        """重新设置会话"""
        self.session = requests.Session()

    def __reset_current_headers(self):
        """重新设置当前请求头"""
        self.__current_headers = self.headers_manager.get()
