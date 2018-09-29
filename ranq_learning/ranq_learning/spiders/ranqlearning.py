# -*- coding: utf-8 -*-
import scrapy
from ..items import RanqLearningItem
#from bs4 import BeautifulSoup
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import json
import re
import requests

#URL='http://192.168.33.10:3000/api/hode?holder=dff&pages=%d'
URL='http://ranq-media.com/api/hode?holder=dff&page=%d'
class RanqlearningSpider(scrapy.Spider):
    name = 'ranq_learning'
    allowed_domains = ['ranq-media.com']

    def start_requests(self):
        r = requests.get(URL % 1)
        data = r.json()
        pages = data[0]["pages"]
        for page in range(1,pages+1):
            yield scrapy.Request(URL % page, self.parse)

    def parse(self, response):

        jsonresponse = json.loads(response.body_as_unicode())
        p = re.compile(r"<[^>]*?>")
        for article in jsonresponse[0]["articles"]:
            item = RanqLearningItem()
            item["id"]=str(article["id"])
            item["title"]= article["title"]
            item["description"]= p.sub("",article["description"]).replace(" ","")
            item["user_id"]= str(article["user_id"])
            item["category"]= article["category"]
            item["view"]= str(article["view_count"])
            yield item
