"""用于爬虫的装饰器
"""
from CrawlER import CrawlerType

task_queue_list = []


def config(spacing_time=0, timeout=20, type_=CrawlerType.html, collection_name="", err_collection_name=""):
    """
    用于爬虫设定的装饰器
    :param spacing_time: 爬虫间隔时间
    :param timeout:超时设置
    :param type_: 请求类型
    :param collection_name: 集合名
    :param err_collection_name: 收集异常的集合名称
    :return:
    """
    def decorator(func):
        def get_task_queue_kwargs():

            # 确定异常集合名
            if err_collection_name:
                _err_collection_name = err_collection_name
            elif collection_name:
                _err_collection_name = "".join([collection_name, "_error"])
            else:
                _err_collection_name = "".join([func.__name__, "_error"])

            return {
                "func": func,
                "timeout": timeout,
                "type": type_,
                "spacing_time": spacing_time,
                "collection_name": collection_name or func.__name__,
                "err_collection_name": _err_collection_name
            }

        # Crawler生成时, 确认是否为爬虫函数的标志
        get_task_queue_kwargs.task_func = True
        return get_task_queue_kwargs

    return decorator


if __name__ == '__main__':
    class TestMeta(type):
        def __new__(mcs, name, bases, attrs):
            task_func_list = []
            [task_func_list.append(v) if hasattr(v, "task_func") else None for k, v in attrs.items()]
            task_queue_list = [_(None) for _ in task_func_list]
            attrs.update({"task_queue_list": task_queue_list})

            return type.__new__(mcs, name, bases, attrs)


    class Test1(object, metaclass=TestMeta):
        def __init__(self):
            pass

        @config(spacing_time=2, is_crawl_file=False)
        def test1(self):
            print("laal")

        @config(spacing_time=3)
        def test2(self):
            print("fdafsdf")


    print("2")
    t = Test1()

    print(t.task_queue_list)

    print(t.test2())
    t.test2()["func"](t)

    print(t.test1())
    t.test1()["func"](t)
