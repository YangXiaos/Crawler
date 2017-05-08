"""任务队列
封装mongodb 的任务队列对象
"""
import threading

from CrawlER.CrawlTaskManager.RequestTask import RequestTask


class TaskQueue(object):
    """任务队列
    从队列中获取任务, 任务异常的更新

    Attributes:
        mutex: 线程锁
        err_collection: 数据库异常集合
        collection: 数据库集合
        func: 处理方法

        spacing_time: 爬虫请求间隔时间
        crawl_file: 是否为爬取文件请求
        record_error: 是否记录异常

    Methods:
        get: 获取任务
        put: 更新任务
        qsize: 任务数量
        is_empty: 是否为空
    """
    def __init__(self, collection_, func, err_collection=None, spacing_time=0, is_crawl_file=False):
        self.mutex = threading.Lock()
        self.collection = collection_
        self.err_collection = err_collection
        self.func = func

        self.spacing_time = spacing_time
        self.crawl_file = is_crawl_file

    def get(self):
        """获取任务"""
        self.mutex.acquire() # 线程锁获取队列任务, 防止重复获取
        task_params = self.collection.find_one_and_delete({})
        self.mutex.release()

        return RequestTask(self, **task_params)

    def put(self, url, **other):
        """
        更新任务队列
        :param url: 任务url
        :param other: 其他相关参数
        :return:
        """
        document = {"url": url}
        document.update(other)

        self.collection.insert_one(document)

    def qsize(self):
        return self.collection.count()

    def update_error(self, task_params, error):
        """
        记录异常
        :param task_params:
        :param error:
        :return:
        """
        task_params.update({"error": error})
        self.err_collection.insert_one(task_params)

    @property
    def is_empty(self):
        """判断是否为空"""
        return True if not self.qsize() else False


if __name__ == '__main__':
    from pymongo import *

    def test():
        print("测试")

    client = MongoClient()
    db = client.test
    coll = db["yang"]

    q = TaskQueue(coll, test)
    q.put("www.ccav.com", **{"dir_": "base"})
    print(q.qsize())
    print(q.is_empty)
    print(q.get())
