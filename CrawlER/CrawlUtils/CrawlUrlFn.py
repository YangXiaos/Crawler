# @Time         : 17-9-3 下午7:22
# @Author       : DioMryang
# @File         : CrawlUrlFn.py
# @Description  : url 方法函数

from urllib.parse import urljoin


def get_all_url(res, crawler, part_of_url):
    """
    获取完整的url

    part_of_url的形式:
        http://www.ex.com or https://www.ex.cn
        www.ex.com
        tag/123
        /tag/123

    :param res: 请求
    :param url: 请求链接
    :param crawler: 爬虫架构
    :param part_of_url: url部分
    :return:
    """
    # 完整的url
    if part_of_url.startswith("http://") or part_of_url.startswith("https://"):
        return part_of_url

    # www开头
    if part_of_url.startswith("/"):
        crawler

