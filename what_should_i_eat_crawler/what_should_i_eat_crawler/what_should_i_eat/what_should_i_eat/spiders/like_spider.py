import scrapy
from bs4 import BeautifulSoup


class LikeSpider(scrapy.Spider):

    name = "like"

    def start_requests(self) -> scrapy.Request:
        urls = []
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: scrapy.http.Response):
        """
        @url https://www.sirogohan.com/recipe/wahuukare-/
        """
        print("url : ", response.url)
