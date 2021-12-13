
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import os
from typing import Dict

import scrapy # type: ignore
from what_should_i_eat import settings


OUTPUT_DIR = os.path.join(settings.PROJECT_ROOT, "input")


class WhatShouldIEatPipeline:
    def process_item(self, item: Dict, spider: scrapy.Spider) -> None:
        adapter = ItemAdapter(item)
        print("adapter")
        print(adapter)
        
        if adapter["category"] == "like":
            self.output_csv("likes_recipe.tsv", adapter)
        elif adapter["category"] == "dislike":
            self.output_csv("dislikes_recipe.tsv", adapter)
        elif adapter["category"] == "eval":
            self.output_csv("eval.tsv", adapter)
        else:
            raise NotImplementedError("Error adapter.get(category)")
            
        return None

    def output_csv(self, filename: str, adapter: ItemAdapter) -> None:
        filepath = os.path.join(OUTPUT_DIR, filename)
        print("filepath : ", filepath)
        with open(filepath, "a", encoding="utf-8") as w:
            w.write(adapter["title"] + "\t" + adapter["recipe"])
            w.write("\n")

        return None
