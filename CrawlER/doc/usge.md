```
import CrawlER

from CrawlER import ResquestTask
from CrawlER import config


class Cartoon(CrawlER.Crawler):
    """图片抓取任务"""
    db_name = "name"
    worker_num = 3
    start_url = []
    
    user_agent_list = [
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
    ]
    
    
    @config(spacing_time=1, error_record=True)
    def start(self, res, soup):
        ...
        self.setTask(url, callback=self.next, **params)
        
    @config(spacing_time=1, crawl_file=True)
    def next(self, res, soup, **kwargs):
        ...

```