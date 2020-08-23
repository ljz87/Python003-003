# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from spiders.items import SpidersItem

class MoviesSpider(scrapy.Spider):
    # 定义爬虫名称
    name = 'movies'
    allowed_domains = ['maoyan.com']
    start_urls = ['http://maoyan.com/films?showType=3']

#   注释默认的parse函数
#   def parse(self, response):
#        pass

    # 爬虫启动时，引擎自动调用该方法，并且只会被调用一次，用于生成初始的请求对象（Request）。
    # start_requests()方法读取start_urls列表中的URL并生成Request对象，发送给引擎。
    # 引擎再指挥其他组件向网站服务器发送请求，下载网页
    def start_requests(self):
            url = f'http://maoyan.com/films?showType=3'
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=False)
            # url 请求访问的网址
            # callback 回调函数，引擎回将下载好的页面(Response对象)发给该方法，执行数据解析
            # 这里可以使用callback指定新的函数，不是用parse作为默认的回调参数

    # 解析函数
    def parse(self, response):
        # 打印网页的url
        #print(response.url)
        # 打印网页的内容
        #print(response.text)
        
        # 找出电影链接地址
        movies = Selector(response=response).xpath('//dd/div[@class="movie-item film-channel"]/a')
        
        # 提取前10个电影地址，并请求该页面
        for movie in movies[:10]:
            # 实际网页上提取的地址是不全的，这里进行地址补全
            link = 'https://maoyan.com'+ movie.xpath('@href').extract()[0]
            print(link)

            item = SpidersItem()
            item['link'] = link
            yield scrapy.Request(url=link, meta={'item': item}, callback=self.parse2)

    # 解析具体页面
    def parse2(self, response):
        # 打印网页的url
        # print(response.url)
        item = response.meta['item']
        movies = Selector(response=response).xpath('//div[@class = "movie-brief-container"]')

        MovieName = movies.xpath('./h1[@class = "name"]/text()').extract()[0]
        print(MovieName)

        movies = movies.xpath('./ul/li[@class="ellipsis"]')

        MvType = movies.xpath('./a[@class="text-link"]/text()')
        MovieType = ''

        for Type in MvType:
            if MovieType == '' :
                MovieType = Type.extract().lstrip().rstrip()
            else:
                MovieType = MovieType + '/' + Type.extract().lstrip().rstrip()

        print(MovieType)

        MovieDate = movies[2].xpath('./text()').extract()[0][:10]

        print(MovieDate)
        
        item['name'] = MovieName
        item['style'] = MovieType
        item['date'] = MovieDate
        
        yield item
