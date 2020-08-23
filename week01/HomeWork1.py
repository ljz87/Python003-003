# 使用BeautifulSoup解析网页

import requests
from bs4 import BeautifulSoup as bs
# bs4是第三方库需要使用pip命令安装

def getMovieInfo( url , movielist ):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    header = {'user-agent':user_agent}
    response = requests.get(url,headers=header)
    bs_info = bs(response.text, 'html.parser')

    #with open(url, 'r',encoding='UTF-8') as f:
    #    bs_info = bs(f.read(), 'html.parser')

    for tags in bs_info.find_all('div', attrs={'class': 'movie-brief-container'}):
        MovieType = ''

        # 获取电影名称
        for atag in tags.find_all('h1'):
            MovieName= atag.string

        # 获取电影类型
        for litag in tags.find_all('li'):
            for atag in litag.find_all('a'):
                if MovieType == '' :
                    MovieType = atag.string.lstrip().rstrip()
                else:
                    MovieType = MovieType + '/' + atag.string.lstrip().rstrip()

        # 获取上映时间
        MovieDate = litag.string[:10]
        
        movielist.append([MovieName,MovieType,MovieDate])


user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
header = {'user-agent':user_agent}
myurl = 'https://maoyan.com/films?showType=3'
response = requests.get(myurl,headers=header)
bs_info = bs(response.text, 'html.parser')

# path = './Web/01/maoying.html'

# with open(path, 'r',encoding='UTF-8') as f:
#     bs_info = bs(f.read(), 'html.parser')

MovieUrls = []

#print(bs_info)

# Python 中使用 for in 形式的循环,Python使用缩进来做语句块分隔
for tags in bs_info.find_all('div', attrs={'class': 'movie-item film-channel'}):
    for atag in tags.find_all('a'):
        MovieUrls.append('https://maoyan.com'+atag.get('href'))

#print(MovieUrls)

MovieList = []

from time import sleep

sleep(10)

# 找出前10的电影，并将电影名称、类型和上映时间以 UTF-8 字符集保存到 csv 格式的文件中。
for i in range(0,20,2):
    #print(MovieUrls[i])
    # 获取电影名称、类型和上映时间
    getMovieInfo(MovieUrls[i],MovieList)
    sleep(5)

#保存到csv文件中

print(MovieList)

import pandas as pd

Movie1 = pd.DataFrame(data = MovieList)

Movie1.to_csv('./movie1.csv', encoding='utf8', index=False, header=False)