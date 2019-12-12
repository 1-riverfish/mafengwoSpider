# /usr/bin/python
# -*- coding: utf-8 -*-
# @Time         : 2019/12/9
# @Author       : jwy
# @Email        : lygjwy@qq.com
# @Description  : 根据马蜂窝游记内容分析

import os
import numpy as np
import re


class ContentAnalyser:
    # 游记内容分析类
    matrix = np.zeros([19, 19])
    files = []
    visitList = ["海口", "三亚", "文昌", "琼海", "万宁", "三沙", "儋州", "东方", "五指山", "定安", "屯昌", "澄迈", "临高", "陵水", "琼中", "保亭", "白沙",
                 "乐东", "昌江"]

    def __init__(self):
        self.files = os.listdir("contents")

    def routeAnalyse(self):
        for file in self.files:
            f = open("contents"+"/"+file, encoding='utf-8')
            content = f.readline()
            # 先把数字全部找出来替换为空格
            content = re.sub("[0-9]", str(""), content, 0, 0)
            # print(content)

            # 再用数字替换景点
            #  进行景点顺序解析
            count = 0
            for visit in self.visitList:
                content = re.sub(visit, str(count), content, 0, 0)
                count += 1
            #  检验一下是否将景点替换为数字
            # print(content)

            # 得到数字列表即对应顺序  下边这种正则写的方式有问题
            #  提取元文本中的数字
            sequenceList = re.findall("\d+", content, flags=0)
            #  检验提取数字的顺序  没有问题
            print(sequenceList)

            #  根据相邻元素填写矩阵
            size = len(sequenceList)
            for num in range(0, size - 1):
                num1 = int(sequenceList[num])
                num2 = int(sequenceList[num + 1])
                if num1 != num2:
                    self.matrix[num1 % 19][num2 % 19] += 1
        np.savetxt('matrix.csv', self.matrix, delimiter=',')


if __name__ == "__main__":
    contentAnalyser = ContentAnalyser()
    contentAnalyser.routeAnalyse()