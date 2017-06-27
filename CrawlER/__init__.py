""""""
from enum import Enum, unique


@unique
class CrawlerType(Enum):
    file = 0
    json = 1
    html = 2
    post = 3
    driver = 4

