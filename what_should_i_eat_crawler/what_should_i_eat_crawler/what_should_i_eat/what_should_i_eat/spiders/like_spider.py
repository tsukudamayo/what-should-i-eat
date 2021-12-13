import json
import os
from typing import Iterable, Dict, List

import scrapy # type: ignore
from bs4 import BeautifulSoup # type: ignore

from what_should_i_eat import settings


DATA_DIR = settings.PROJECT_ROOT
LIKE_FILE = os.path.join(DATA_DIR, "input", "likes.json")
DISLIKE_FILE = os.path.join(DATA_DIR, "input", "dislikes.json")

class LikeSpider(scrapy.Spider):

    name = "like"

    def start_requests(self) -> Iterable[scrapy.Request]:
        dataset = [LIKE_FILE, DISLIKE_FILE]
        functions = [self.parse_likes, self.parse_dislikes]
        urls: List[str] = []
        for d, f in zip(dataset, functions):
            with open(d) as r:
                data = json.load(r)
                urls = data
                for url in urls:
                    yield scrapy.Request(url=url, callback=f)

    def parse_likes(self, response: scrapy.http.Response) -> Iterable[Dict]:
        """
        @url https://www.sirogohan.com/recipe/wahuukare-/
        @returns item 1 1
        @scrapes title recipe category
        """
        item = self.fetch_title_and_recipe(response)
        item["category"] = "like"

        yield item

    def parse_dislikes(self, response: scrapy.http.Response) -> Iterable[Dict]:
        """
        @url https://www.sirogohan.com/sp/recipe/kabochagohan/
        @returns item 1 1
        @scrapes title recipe category
        """
        item = self.fetch_title_and_recipe(response)
        item["category"] = "dislike"

        yield item

    def fetch_title_and_recipe(self, response: scrapy.http.Response) -> Dict:
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

        return item
