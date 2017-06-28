"""
用于爬虫请求的函数
"""
import chardet
from bs4 import BeautifulSoup

from CrawlER.Exception.RequestException import StateCodeException


class FileSoup(object):
    """图片解析
    Methods:
        get_file_name: 获取文件名
        get_file_suffix: 获取后缀
        save: 保存文件
    """

    def __init__(self, content, res):
        self.content = content
        self.res = res

    def get_file_name(self):
        """获取文件名"""
        return self.res.url.split("/")[-1]

    def get_file_suffix(self):
        """获取文件后缀"""
        return self.res.url.split(".")[-1]

    def save(self, path):
        """
        保存文件
        :param path: 路径
        :return:
        """
        with open(path, 'wb') as f:
            for chunk in self.content:
                if chunk:
                    f.write(chunk)
                    f.flush()


def parse_html(content, parser="lxml"):
    """
    解析网页
    :param content: 网页内容
    :param parser: 解析器
    :return: 解析后的html_soup
    """
    return BeautifulSoup(content, parser)


def parse_file(content, res):
    """
    解析文件soup
    :param content: 文件content
    :param res: 请求头
    :return: 返回伪解析的soup
    """
    return FileSoup(content, res)


def crawl_html(session, url, timeout=20, **kwargs):
    """
    爬取html页面
    :param session: 会话
    :param url: 链接
    :param timeout: 超时设置
    :param kwargs: 额外参数
    :return:
    """
    res = session.get(url, timeout=timeout, **kwargs)

    # 编码设定
    res.encoding = chardet.detect(res.content)["encoding"]

    # 状态码错误
    if res.status_code != 200:
        raise StateCodeException("状态码错误{}".format(res.status_code))

    return res


def crawl_file(session, url, timeout=20, **kwargs):
    """
    抓取文件类型请求
    :param session: 会话
    :param url: 链接
    :param timeout: 超时设置
    :param kwargs: 额外参数
    :return: 返回请求结果
    """
    res = session.get(url, timeout=timeout, stream=True, **kwargs)

    # 状态码错误
    if res.status_code != 200:
        raise StateCodeException("状态码错误{}".format(res.status_code))

    return res


def json_request(session, url, timeout=20, **kwargs):
    """
    json 请求
    :param session: 会话
    :param url: 请求链接
    :param timeout: 超时设置
    :param kwargs: 其他请求参数
    :return:
    """
    res = session.get(url, timeout=timeout, **kwargs)

    # 状态码异常
    if res.status_code != 200:
        raise StateCodeException("状态码错误{}".format(res.status_code))

    return res.json()



if __name__ == '__main__':
    import requests

    session = requests.Session()
    res = session.get("http://wx3.sinaimg.cn/mw600/a905b8d7gy1fff6bu2knqj20c805x3za.jpg")


