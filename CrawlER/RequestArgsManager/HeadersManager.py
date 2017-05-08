"""浏览器头管理者
"""
import random


class HeadersManager(object):
    """

    Attributes:
        headers_list: 浏览器头列表

    Methods:
        get: 获取请求头
    """
    def __init__(self, headers_list):
        self.headers_list = headers_list

    def get(self):
        return random.choice(self.headers_list)
