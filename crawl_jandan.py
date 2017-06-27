# @Time         : 17-5-9 下午5:08
# @Author       : DioMryang
# @File         : crawl_jandan.py
# @Description  : 爬取煎蛋网图片的脚步
from CrawlER.CrawlUtils.CrawlDecorator import config
from CrawlER.Crawler import Crawler


class JanDanCrawler(Crawler):
    """
    煎蛋无聊图爬虫
    """
    start_url = ["http://jandan.net/pic/page-{}#comments".format(_) for _ in range(1, 241)]
    user_agent = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36")
    db_name = "JanDan"

    @config(spacing_time=2, timeout=20)
    def start(self, res, soup, **other):
        """爬取图片地址"""
        for href in [tag["href"] for tag in soup.select("a.view_img_link")]:
            self.set_task("http:"+href, "downland_img")

    @config(spacing_time=1, timeout=20, is_crawl_file=True)
    def downland_img(self, res, soup, **other):
        """爬取图片"""
        soup.save("items/"+soup.get_file_name())


crawler = JanDanCrawler()
crawler.begin()