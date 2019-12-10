# /usr/bin/python
# -*- coding: utf-8 -*-
# @Time         : 2019/12/10
# @Author       : jwy
# @Email        : lygjwy@qq.com
# @Description  : 根据游记链接使用Selenium模拟下拉操作爬取游记内容

from selenium import webdriver
import time
import random

class SeleniumSpider:
    urlList = []

    def __init__(self, path):
        self.driver = webdriver.Chrome()
        f = open(path, "r")
        self.urlList = f.readlines()
        f.close()

    def scrapyYj(self):
        i = 1
        for url in self.urlList:
            self.driver.get(url)
            # 等待界面加载完成
            # 可以改进
            time.sleep(5)
            # 滚动到页面最底部
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(5)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            # get specific <p>
            ps = self.driver.find_elements_by_xpath("//p[@class='_j_note_content _j_seqitem']")
            # 提取内容并保存到本地
            content = ""
            for p in ps:
                # remove space and \n
                content = content + p.text.strip().replace("\n", "").replace(" ", "")
            self.yjContentUtil(str(i), content)
            print("Yj: "+str(i))
            print(content)
            i = i + 1
            time.sleep(random.randint(0, 1))

    def yjContentUtil(self, name, content):
        f = open("./contents/"+name+".txt", "w", encoding='utf-8')
        f.write(content)
        f.close()


if __name__ == "__main__":
    # 爬取游记内容
    seleniumSpider = SeleniumSpider("ygUrls.txt")
    seleniumSpider.scrapyYj()