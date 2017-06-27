# @Time         : 17-5-9 下午5:08
# @Author       : DioMryang
# @File         : crawl_jandan.py
# @Description  : 爬取煎蛋网图片的脚步
from CrawlER.CrawlUtils.CrawlDecorator import config
from CrawlER.Crawler import Crawler


good_img_dir = "MeiZi/1/"
normally_img_dir = "MeiZi/2/"
bad_img_dir = "MeiZi/3/"


class JanDanCrawler(Crawler):
    """
    煎蛋无聊图爬虫
    """
    start_url = ["http://jandan.net/ooxx/page-{}#comments".format(_) for _ in range(1, 46)]
    user_agent = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                  " (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36")
    db_name = "JanDanMeiZi"

    @config(spacing_time=2, timeout=20)
    def start(self, res, soup, **other):
        """爬取图片地址"""
        for li_tag in soup.select(".commentlist li"):
            # 判断该li是否有图片
            if not li_tag.select_one("img"):
                continue

            # 获取投票数, 比例
            _, up_vote, down_vote, *_ = li_tag.select(".vote span")
            up_num, down_num, ratio =int(up_vote.string), int(down_vote.string), int(up_vote.string)/int(down_vote.string)

            # 分配图片目录
            if ratio > 2 or up_num>50:
                params = {"path": good_img_dir}
            elif 2 > ratio >= 1:
                params = {"path": normally_img_dir}
            else:
                params = {"path": bad_img_dir}

            self.set_task("http:"+li_tag.select_one("img")["src"], callback="downland_img", **params)

    @config(spacing_time=1, timeout=20, is_crawl_file=True)
    def downland_img(self, res, soup, **other):
        """爬取图片"""
        soup.save(other.get("path") + soup.get_file_name())


crawler = JanDanCrawler()
crawler.begin()