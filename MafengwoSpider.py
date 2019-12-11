# /usr/bin/python
# -*- coding: utf-8 -*-
# @Time         : 2019/12/8
# @Author       : jwy
# @Email        : lygjwy@qq.com
# @Description  : 爬取马蜂窝指定目的地游记链接

import os
import random
import requests
import time
from bs4 import BeautifulSoup
import lxml

import ContentAnalyser
import SeleniumSpider


class MafengwoSpider:

    urlPrefix = "http://www.mafengwo.cn/yj/"
    yjUrlPrefix = "http://www.mafengwo.cn"
    uaList = [
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:21.0) Gecko/20100101 Firefox/21.0',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:21.0) Gecko/20130331 Firefox/21.0',
        'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 '
        'Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 '
        'Chrome/27.0.1453.93 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
        'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
        'Mozilla/5.0 (compatible; WOW64; MSIE 10.0; Windows NT 6.2)',
        'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.9.168 Version/11.52',
        'Opera/9.80 (Windows NT 6.1; WOW64; U; en) Presto/2.10.229 Version/11.62',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_6; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) '
        'Version/5.0.4 Safari/533.20.27',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 '
        'Safari/533.20.27',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 '
        'Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 '
        'Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 '
        'Safari/602.2.14',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 '
        'Safari/537.36 Qiyu/2.1.0.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.87 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.3 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 '
        'Safari/537.36 Qiyu/2.1.0.0',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 '
        'Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 '
        'Safari/537.36 '
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'
    ]

    headers = {
        'Referer': 'http://www.mafengwo.cn/',
        'Upgrade-Insecure-Requests': '1'
    }

    yjUrlList = []
    yjContentList = []

    def __init__(self, id, page):
        # 目的地id
        self.id = id
        self.page = page
        self.session = requests.Session()
        self.urlPart = self.urlPrefix + str(self.id) + "/1-0-"

    def yjUrlScraper(self):
        # 爬取所有的游记url
        for i in range(1, self.page+1):
            print("Page: "+str(i))
            url = self.urlPart + str(i) + ".html"
            self.headers['User-Agent'] = random.choice(self.uaList)
            response = self.session.get(url, headers=self.headers)

            if response.status_code == 200:
                # print("PageUrl "+url)
                soup = BeautifulSoup(response.text, "lxml")
                # need parser
                self.yjUrlParser(soup)
            else:
                exit()

            # avoid anti-scrapy
            # time.sleep(random.randint(1, 2))

        # 持久化，保存游记链接到本地
        self.yjUrlUtil()

    def yjUrlParser(self, soup):
        # 解析每一页面中的游记链接
        aList = soup.find_all("a", {'class': "title-link"})
        print(len(aList))
        for a in aList:
            self.yjUrlList.append(self.yjUrlPrefix+a["href"])

    def yjUrlUtil(self):
        # 将游记url去重并保存到本地文件
        print("Total number of yj before remove repeat: "+str(len(self.yjUrlList)))
        self.yjUrlList = list(set(self.yjUrlList))
        print("Total number of yj after remove repeat: "+str(len(self.yjUrlList)))
        file = open("ygUrls.txt", 'w')
        for yjUrl in self.yjUrlList:
            file.write(yjUrl+"\n")
        file.close()


if __name__ == "__main__":
    # 爬虫第一个参数为目的地Id，第二个参数为游记页数，默认爬取最热游记，数量上限为3k
    mafengwoSpider = MafengwoSpider(12938, 186)

    # 首先爬取游记链接
    mafengwoSpider.yjUrlScraper()































