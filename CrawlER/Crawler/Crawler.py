"""爬虫Crawler
"""
from pymongo import *
import time
import traceback
import requests

from CrawlER import CrawlerType
from CrawlER.CrawlUtils.CrawlRequest import crawl_file, crawl_html, json_request, parse_file, parse_html
from CrawlER.Exception import WithOutEnoughTask, CrawlException

from CrawlER.CrawlTaskManager.TaskQueue import TaskQueue, TaskQueueManager
from CrawlER.CrawlRecord.CrawlRecordManager import CrawlRecordManager


class CrawlerMeta(type):
    """
    Crawler Meta
    """
    def __new__(mcs, name, bases, attrs):
        # 获取任务队列列表

        if name == "Crawler":
            return type.__new__(mcs, name, bases, attrs)

        task_queue_list = []
        db = MongoClient()[attrs.get("db_name")]

        # 获取生成任务队列的函数列表
        task_queue_generate_list = []
        for k, v in attrs.items():
            if hasattr(v, "task_func"):
                task_queue_generate_list.append(v)

        # 更新任务队列
        for func in task_queue_generate_list:
            task_queue_kwargs = func()
            collection_name, err_collection_name = \
                task_queue_kwargs["collection_name"], task_queue_kwargs["err_collection_name"]

            collection_ = db[collection_name]
            err_collection = db[err_collection_name]
            task_queue_list.append(
                TaskQueue(collection_,
                          err_collection,
                          task_queue_kwargs.get("func"),
                          task_queue_kwargs.get("spacing_time"),
                          task_queue_kwargs.get("timeout"),
                          task_queue_kwargs.get("type"))
            )

        attrs.update({"task_queue_list": task_queue_list})
        attrs.update({"db": db})
        return type.__new__(mcs, name, bases, attrs)


class Crawler(object, metaclass=CrawlerMeta):
    """
    爬虫架构

    GlobalAttributes:
        db_name: 数据库名
        task_queue_list: 任务队列列表
        start_url: 开始urls
        worker_num: 工作者数量
        spacing_time: 每个工作者间隔时间
        timeout: 超时设置
        session: 请求Session

    Attributes:
        db: 数据库
        task_manager: 任务管理器
        crawl_record_manager: 爬虫记录管理者
        headers: 请求头

    Methods:
        set_task: 添加任务
        crawl: 一次爬虫请求
        begin: 开始请求爬虫
        __set_start_task_queue: 设置初始爬虫任务队列

    """
    db_name = ""
    start_url = []
    user_agent = ""

    def __init__(self):
        self.crawl_record_manager= CrawlRecordManager(self.db)
        self.task_manager = TaskQueueManager(self.task_queue_list)
        self.headers = {"User-Agent": self.user_agent}
        self.session = requests.Session()

        # 添加初始任务url
        if not self.crawl_record_manager.is_start:
            self.__set_start_task_queue()

    def __set_start_task_queue(self):
        """设置初始任务队列"""
        for _ in self.start_url:
            self.task_manager.find_task_queue_by_name("start").put(_)

        self.crawl_record_manager.set_start_flat()

    def set_task(self, url, callback, **params):
        """
        设置下个任务
        :param url: 请求链接
        :param callback: 回调函数名
        :param params: 其他任务参数
        :return:
        """
        self.task_manager.find_task_queue_by_name(callback).put(url, **params)

    def crawl(self, crawl_task):
        """
        单次爬虫请求
        :param crawl_task: 爬虫任务
        :return:
        """
        if crawl_task.type == CrawlerType.html:
            res = crawl_html(self.session, crawl_task.request_url, crawl_task.timeout, headers=self.headers)
            soup = parse_html(res.content)
            crawl_task.func(self, res, soup, **crawl_task.request_params)

        elif crawl_task.type == CrawlerType.file:
            res = crawl_file(self.session, crawl_task.request_url, crawl_task.timeout, headers=self.headers)
            soup = parse_file(res.iter_content(chunk_size=1024), res)
            crawl_task.func(self, res, soup, **crawl_task.request_params)

        elif crawl_task.type == CrawlerType.json:
            res = crawl_html(self.session, crawl_task.request_url, crawl_task.timeout, headers=self.headers)
            json_data = res.json()
            crawl_task.func(self, res, json_data, **crawl_task.request_params)

        elif crawl_task.type == CrawlerType.res:
            res = crawl_html(self.session, crawl_task.request_url, crawl_task.timeout, headers=self.headers)
            crawl_task.func(self, res, **crawl_task.request_params)

        time.sleep(crawl_task.spacing_time)

    def begin(self):
        """
        开始爬虫任务
        :return:
        """
        while True:
            try:
                crawl_task = self.task_manager.get_task()
                self.crawl(crawl_task)
            except WithOutEnoughTask:
                print("爬取结束")
                break
            except Exception as e:
                crawl_task.record_error(traceback.format_exc())

    def start(self, res, soup, **other):
        """"""
        pass

if __name__ == '__main__':
    from CrawlER.CrawlUtils.CrawlDecorator import config

    class Test(Crawler):
        user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36"
        db_name = "test2"
        start_url = ["http://python.usyiyi.cn/django/index.html"]

        @config(spacing_time=0, collection_name="start_collection", err_collection_name="start_err_collection")
        def start(self, res, soup, **other):
            self.set_task("http://python.usyiyi.cn/django/index.html", callback="to")

        @config(spacing_time=5, collection_name="get_collection")
        def to(self, res, soup, **params):
            print(res.url)

    t = Test()
    t.begin()

