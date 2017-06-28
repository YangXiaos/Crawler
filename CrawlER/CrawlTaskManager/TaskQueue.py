"""任务队列
封装mongodb 的任务队列对象
"""
import threading

from CrawlER import CrawlerType
from CrawlER.Exception import WithOutEnoughTask
from CrawlER.CrawlTaskManager.RequestTask import RequestTask


class TaskQueue(object):
    """任务队列
    从队列中获取任务, 任务异常的更新

    Attributes:
        mutex: 线程锁
        err_collection: 数据库异常集合
        collection: 数据库集合
        func: 处理方法

        timeout: 超时设置
        spacing_time: 爬虫请求间隔时间
        type: 请求类型

    Methods:
        get: 获取任务
        put: 更新任务
        qsize: 任务数量
        is_empty: 是否为空
    """
    def __init__(self, collection_, err_collection, func, spacing_time=0, timeout=20, type_=CrawlerType.html):
        # 线程锁
        self.mutex = threading.Lock()

        # 数据集合, 异常集合, 请求方法
        self.collection, self.err_collection, self.func = collection_, err_collection, func

        # 请求参数, 请求类型
        self.timeout, self.spacing_time, self.type = timeout, spacing_time, type_

    def get(self):
        """获取任务"""
        # 线程锁获取队列任务, 防止重复获取
        self.mutex.acquire()
        task_params = self.collection.find_one_and_delete({})
        self.mutex.release()

        return RequestTask(self, task_params)

    def put(self, url, **task_params):
        """
        更新任务队列
        :param url: 任务url
        :param task_params: 其他相关参数
        :return:
        """
        document = {"url": url}
        document.update(task_params)
        self.collection.insert_one(document)

    def qsize(self):
        """返回集合数量"""
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


class TaskQueueManager(object):
    """
    任务队列管理者, 负责对任务队列进行管理

    Attributes:
        collection_dict: 任务队列映射
        task_queue_list: 任务队列<TaskQueue object >的列表
        __current_task_queue: 当前任务队列

    Methods:
        find_task_queue_by_name: 根据函数名查找集合
        get_task: 获取任务
        is_crawled: 是否爬取过
        __set_current_task_queue: 设置当前的任务队列

    """
    def __init__(self, task_queue_list):
        self.task_queue_list = task_queue_list
        self.collection_dict = {}
        self.__current_task_queue = None

        # 设置函数名及对应任务队列映射
        for task_queue in task_queue_list:
            self.collection_dict.update({task_queue.func.__name__: task_queue})

    def find_task_queue_by_name(self, func_name):
        """
        根据对应函数名查找对应mongodb的task_queue
        :param func_name: 函数名
        :return: 返回task_queue
        """
        return self.collection_dict[func_name]

    def get_task(self):
        """获取任务, 返回对应任务及对应处理函数, """
        # 判断当前是否有任务队列, 或任务队列的数量是否为零, 如果为零重新设置任务队列
        if self.__current_task_queue is None or self.__current_task_queue.is_empty:
            self.__set_current_task_queue()
        return self.__current_task_queue.get()

    def __set_current_task_queue(self):
        """设置当前任务队列"""
        # print(self.task_queue_list)
        for task_queue in self.task_queue_list:
            # 判断是否为空队列
            # print("任务是否为空", task_queue.is_empty)
            if not task_queue.is_empty:
                self.__current_task_queue = task_queue
                return
        raise WithOutEnoughTask("没有足够任务参数")


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
