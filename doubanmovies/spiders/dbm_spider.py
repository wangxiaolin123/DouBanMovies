# coding: utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import json

import scrapy
from scrapy.linkextractors import LinkExtractor

from doubanmovies.items import DoubanmoviesItem, DirectorItem


class myspider(scrapy.Spider):
    start = 0
    name = r'moviespider'
    allowed_domains = [r'movie.douban.com']
    start_urls = [r'https://movie.douban.com/']

    # rules = (
    #     # 符合规则的url请求返回函数为parse_item，并跟进，response传下去继续匹配
    #     Rule(LinkExtractor(allow=(r'https://movie.douban.com/subject/\d+/?from=showing')), callback='parse_item',
    #          follow=False),
    #     # 规则的url请求返回函数为detail, 不跟进
    #     # Rule(LinkExtractor(allow=r'position_detail\.php\?id=\d+'), callback='detail', follow=False)
    # )

    def parse(self, resonse):
        datas = resonse.xpath(r'//*[@id="screening"]/div[2]/ul/li')
        for data in datas:
            if data is None:
                continue
            movie_url = data.xpath(r'./ul/li[2]/a/@href').extract_first()

            yield scrapy.Request(str(movie_url), callback=self.parse_movie)

    def parse_movie(self, resonse):
        if resonse.status == 200:
            item = DoubanmoviesItem()
            item['title'] = resonse.xpath('//*[@id="content"]/h1/span[1]/text()').extract_first()
            item['rate'] = resonse.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()').extract_first()
            item['director'] = resonse.xpath('//*[@id="info"]/span[1]/span[2]/a/text()').extract()
            yield item

            directors = resonse.xpath('//*[@id="info"]/span[1]/span[2]/a/@href')
            for director in directors:
                if director is None:
                   # print 'it\' None'
                    continue
                yield scrapy.Request('https://movie.douban.com'+director.extract(),callback=self.parse_director)


    def parse_director(self, response):
        item1 = DirectorItem()
        director_name = response.xpath('//*[@id="content"]/h1/text()').extract_first()
        sex = response.xpath('//*[@id="headline"]/div[2]/ul/li[1]').extract_first()
        constellation = response.xpath('//*[@id="headline"]/div[2]/ul/li[2]').extract_first()

        item1['name'] = director_name
        item1['sex'] = u"保密"
        item1['constellation'] = u"保密"
        if (sex is not None) and str(sex).find(u'性别') != -1:
            if str(sex).find(u'男') != -1:
                item1['sex'] = u'男'
            else:
                item1['sex'] = u'女'
        if (constellation is not None) and str(constellation).find(u'星座') != -1:
            item1['constellation'] = str(constellation)[45:51]
        yield item1

        latest5Movies = response.xpath('//*[@id="recent_movies"]/div[2]/ul[1]/li')
        if latest5Movies is not None:
            for movie in latest5Movies:
                item2 = DoubanmoviesItem()
                item2['title'] = movie.xpath('./div[2]/a/text()').extract_first()
                item2['rate'] = movie.xpath('./div[2]/em/text()').extract_first()
                item2['director'] = director_name
                yield item2



