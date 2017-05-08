"""
File Name   : CrawlRecordManager.py
Description : 爬虫记录管理者
"""


class CrawlRecordManager(object):
    """
    爬虫记录管理者

    Attributes:
        system_collection: 系统集合

    Methods:
        is_start: 已经有爬取记录
        set_start_flat: 设置标志位
    """
    def __init__(self, db):
        self.system_collection = db["system"]

    def is_start(self):
        """
        :return: 返回是否存在爬取记录的布尔值
        """
        return True if self.system_collection.find_one({}) else False

    def set_start_flat(self):
        self.system_collection.insert_one({"start": True})
