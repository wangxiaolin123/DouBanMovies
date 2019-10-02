# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

from concurrent.futures import ThreadPoolExecutor

from doubanmovies.items import DoubanmoviesItem, DirectorItem


class DoubanmoviesPipeline(object):

    def __init__(self):
        self.pool=ThreadPoolExecutor(max_workers=3)

    def process_item(self, item, spider):
        #   写入json
        if isinstance(item,DoubanmoviesItem):
            print u'电影:',item['title']
            self.movie_num+=1
            content = json.dumps(dict(item),ensure_ascii=False)+'\n'
            self.movie_file.write(content)
        elif isinstance(item,DirectorItem):
            print u'导演:',item['name']
            self.director_num += 1
            content = json.dumps(dict(item),ensure_ascii=False)+'\n'
            self.director_file.write(content)

        return item

    def open_spider(self,spider):
        self.movie_file = open("movie.json","w")
        self.movie_num = 0
        self.director_file = open("director.json","w")
        self.director_num = 0

    def close_spider(self,spider):
        print(u'一共保存了{}部电影'.format(self.movie_num))
        print(u'一共保存了{}位导演'.format(self.director_num))
        self.movie_file.close()
        self.director_file.close()
