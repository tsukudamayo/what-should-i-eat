from typing import Iterable, List, Dict


import scrapy # type: ignore
from bs4 import BeautifulSoup # type: ignore


class KikkomanSpider(scrapy.Spider):

    name = "kikkoman"

    def start_requests(self) -> Iterable[scrapy.Request]:
        
        for n in range(1015, 2015):
            url = f"https://www.kikkoman.co.jp/homecook/search/recipe/0000{str(n)}/index.html"
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response: scrapy.http.Response) -> Dict:
        """
        @url https://www.kikkoman.co.jp/homecook/search/recipe/00001014/index.html
        @returns item 1 1
        @scrapes title recipe category
        """
        item = {}
        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string
        recipe_elements = soup.find_all("span", class_="instruction")
        recipe_list = [r.text for r in recipe_elements]
        recipe = "".join(recipe_list)
        print("url : ", response.url)
        print("title : ", title)
        print("recipe : ", recipe)
        item["title"] = title
        item["recipe"] = recipe
        item["category"] = "eval"

        return item
