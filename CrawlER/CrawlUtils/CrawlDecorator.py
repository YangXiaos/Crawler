"""用于爬虫的装饰器
"""

task_queue_list = []


def config(spacing_time=0, is_crawl_file=False):
    """
    用于爬虫设定的装饰器
    :param spacing_time: 爬虫间隔时间
    :param is_record_error: 错误记录
    :param is_crawl_file: 爬取文件
    :return:
    """
    def decorator(func):
        def wrapper(crawler, *args, **kwargs):
            # 设置函数属性, 添加函数参数
            return {
                "func": func,
                "func_name": func.__name__,
                "is_crawl_file": is_crawl_file,
                "spacing_time": spacing_time
            }
        wrapper.task_func = True
        return wrapper
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