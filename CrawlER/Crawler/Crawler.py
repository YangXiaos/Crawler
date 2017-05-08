"""爬虫Crawler
"""
from pymongo import *
import time
import requests

from CrawlER.CrawlUtils.CrawlRequest import crawl_file, crawl_html, parse_file, parse_html
from CrawlER.Exception import WithOutEnoughTask, CrawlException

from CrawlER.CrawlTaskManager.TaskQueue import TaskQueue
from CrawlER.CrawlTaskManager.TaskManager import TaskManager
from CrawlER.RequestArgsManager.HeadersManager import HeadersManager
from CrawlER.CrawlRecord.CrawlRecordManager import CrawlRecordManager
from CrawlER.Crawler import CrawlerWorker


class CrawlerMeta(type):
    """
    Crawler Meta
    """
    def __new__(mcs, name, bases, attrs):
        # 获取任务队列列表
        task_queue_list = attrs.get("task_queue_list")
        db = attrs.get("db")

        # 获取生成任务队列的函数列表
        task_queue_generate_list = []
        for k, v in attrs:
            if v.task_func:
                task_queue_generate_list.append(v)

        # 更新任务队列
        for func in task_queue_generate_list:
            task_queue_kwargs = func(None)
            func_name = task_queue_kwargs.get("func_name")
            collection_ = db[func_name]
            err_collection = db[func_name + "_error"]

            task_queue_list.append(
                TaskQueue(collection_,
                          task_queue_kwargs.get("func"),
                          err_collection,
                          task_queue_kwargs.get("spacing_time"),
                          task_queue_kwargs.get("is_crawl_file"))
            )



class Crawler(object):
    """
    爬虫架构

    GlobalAttributes:
        __db_client: 数据库代理
        db_name: 数据库名
        task_queue_list: 任务队列列表
        start_url: 开始urls
        worker_num: 工作者数量
        spacing_time: 每个工作者间隔时间
        timeout: 超时设置

    Attributes:
        db: 数据库
        task_manager: 任务管理器
        header_manager: 浏览器头
        crawl_record_manager: 爬虫记录管理者

    Methods:
        set_task: 添加任务
        crawl: 一次爬虫请求
        crawl_repeated: 重复爬虫
        begin: 开始请求爬虫
        set_start_task_queue: 设置初始爬虫任务队列

    """
    __db_client = MongoClient()
    db_name = ""
    start_url = []
    worker_num = 1
    user_agent_list = []
    task_queue_list = []

    def __init__(self):
        self.db = self.__db_client[self.db_name]
        self.crawl_record_manager= CrawlRecordManager(self.db)
        self.task_manager = TaskManager(self.task_queue_list)
        self.header_manager = HeadersManager(self.user_agent_list)

        # 添加初始任务url
        if not self.crawl_record_manager.is_start():
            self.set_start_task_queue()

    def set_start_task_queue(self):
        """设置初始任务队列"""
        for _ in self.start_url:
            self.task_manager.find_collection_by_name("start").put(_)


    def set_task(self, url, callback, **params):
        """
        设置下个任务
        :param url: 请求链接
        :param callback: 回调函数名
        :param params: 任务额外参数
        :return:
        """
        self.task_manager.set_task(url, callback, **params)

    def crawl(self):


    def crawl_repeated(self):
        """
        爬取
        :return:
        """
    def begin(self):
        """
        开始爬虫任务
        :return:
        """
        for

