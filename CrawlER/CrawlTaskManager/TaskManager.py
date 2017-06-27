"""任务管理者
从任务队列记录(task_queue_record) 获取信息

从任务队列列表中获取一个任务
"""
from CrawlER.Exception import WithOutEnoughTask


class TaskManager(object):
    """
    任务管理者, 负责对任务队列进行管理

    Attributes:
        collection_dict: 集合字典
        task_queue_list: 任务队列<TaskQueue object >的列表
        __current_task_queue: 当前任务队列

    Methods:
        find_collection_by_name: 根据函数名查找集合
        get_task: 获取任务
        set_task: 设置任务
        is_crawled: 是否爬取过
        __set_current_task_queue: 设置当前的任务队列

    """
    def __init__(self, task_queue_list):
        self.task_queue_list = task_queue_list
        self.collection_dict = {}
        self.__current_task_queue = None

        # 设置
        for task_queue in task_queue_list:
            self.collection_dict.update({task_queue.collection.name: task_queue})

    def find_collection_by_name(self, collection_name):
        """
        根据对应集合名查找对应mongodb的collection
        :param collection_name: 集合名
        :return: 返回collection
        """
        return self.collection_dict[collection_name]

    def get_task(self):
        """获取任务, 返回对应任务及对应处理函数, """
        if self.__current_task_queue is None or self.__current_task_queue.is_empty: # 判断当前任务队列的数量是否为零
            self.__set_current_task_queue()
        return self.__current_task_queue.get()

    def set_task(self, url, collection_name, **other):
        """
        添加任务到对应的任务对列
        :param url: 任务url
        :param collection_name: 集合名
        :param other: 其他额外参数
        :return:
        """
        self.find_collection_by_name(collection_name).put(url, **other)

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

    def add_task_queue(self, task_queue):
        """
        添加任务队列
        :param task_queue: 任务队列
        :return:
        """
        self.task_queue_list.append(task_queue) # 添加任务队列
        self.collection_dict.update({task_queue.collection.name: task_queue}) # 添加集合字典映像


if __name__ == '__main__':
    from pymongo import *
    from CrawlER.CrawlTaskManager.TaskQueue import TaskQueue

    def test():
        print("测试")

    client = MongoClient()
    db = client.test
    coll = db["yang"]

    q = TaskQueue(coll, test)

    taskManager = TaskManager([q])
    taskManager.set_task("www.cctv.com", "yang", **{"dir_": "base"})
    task = taskManager.get_task()
    print(task.url, task.other)
