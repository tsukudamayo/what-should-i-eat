from typing import Iterable, Dict, List

import scrapy # type: ignore
from bs4 import BeautifulSoup # type: ignore


class LikeSpider(scrapy.Spider):

    name = "like"

    def start_requests(self) -> Iterable[scrapy.Request]:
        urls: List[str] = []
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: scrapy.http.Response) -> Iterable[Dict]:
        """
        @url https://www.sirogohan.com/recipe/wahuukare-/
        @returns item 1 1
        @scrapes title recipe
        """
        item = {}
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string
        recipe_elements = soup.find("div", class_="howto-block")\
          .find_all("p")
        recipe_list = [r.text for r in recipe_elements]
        recipe = "".join(recipe_list)
        print("url : ", response.url)
        print("title : ", title)
        print("recipe")
        print(recipe)
        item["title"] = title
        item["recipe"] = recipe

        yield item
