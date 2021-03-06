"""请求任务对象
对mongodb中获取的任务文档进行封装
"""
import copy


class RequestTask(object):
    """请求任务对象封装
    Attributes:
        func: 指向的处理任务的方法函数
        spacing_time: 空闲时间
        crawl_file: 是否为爬取文件请求
        record_error: 是否记录错误
        params: mongodb获取的任务参数
        task_queue: 集合

    Methods:
        request_url: 请求链接
        request_params: 获取任务url外的其他参数
        record_error: 记录当前任务异常
    """
    def __init__(self, task_queue, params):
        self.task_queue = task_queue

        self.func = task_queue.func
        self.spacing_time = task_queue.spacing_time
        self.timeout = task_queue.timeout
        self.type = task_queue.type
        self.params = params

    @property
    def request_url(self):
        """返回请求url"""
        return self.params.get("url")

    @property
    def request_params(self):
        """返回其他参数"""
        params = copy.copy(self.params)
        [params.pop(field_name) for field_name in ["_id", "url"]]
        return params

    def record_error(self, error):
        """
        更新当前任务异常
        :param error:
        :return:
        """
        self.task_queue.update_error(self.params, error)


if __name__ == '__main__':
    def test():
        print("测试")

    task = RequestTask(test, **{"url": "www.ccav.com", "dir_": "base", "_id": 1})
    print(task.request_url)
    print(task.request_params)
    task.func()