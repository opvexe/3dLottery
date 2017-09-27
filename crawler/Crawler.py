#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# -*- author:SHUMIN -*-

import urllib2
import urllib
import re
import xlwt
import xlrd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np

# 解析网页H5数据
def getWebUrl():
    temp = ''
    for index in range(1, 200):
        getUrl = ' http://kaijiang.zhcw.com/zhcw/html/3d/list_' + str(index) + '.html'
        print('请求url: ==' + getUrl)
        requst = urllib.urlopen(getUrl)
        html = requst.read()
        temp = temp + html
    return temp


# 正则法则匹配对应的数据
def reGetHtml():
    temp = getWebUrl()
    reg = re.compile(r'<tr>.*?<td align="center">'
                     r'(.*?)</td>.*?<td align="center">'
                     r'(.*?)</td>.*?<td align="center" '
                     r'style="padding-left:20px;">'
                     r'<em>(.*?)</em>.*?<em>(.*?)</em>.*?'
                     r'<em>(.*?)</em></td>', re.S)
    reScouce = re.findall(reg, temp)
    return reScouce


# 创建excel表格 表格格式为 -- 开奖日期 - 期号 --  百位号码  - 十位号码 -- 个位号码
def creatExcel():
    excel_Head = [u'开奖日期', u'期号', u'百位', u'十位', u'个位']
    wb = xlwt.Workbook()
    ws = wb.add_sheet('3dCaipiao')
    #     创建标题
    index = 0
    for headTitle in excel_Head:
        ws.write(0, index, headTitle)
        index += 1
    # 创建内容
    Content = reGetHtml()
    jndex = 0
    for jdx in excel_Head:
        for index in range(0, len(Content)):
            ws.write(index + 1, jndex, Content[index][jndex])
            index += 1
        jndex += 1

    wb.save("3dMax.xls")


# 获取excel里对应列的数据
def getExcelDate(lie):
    list = []
    date = xlrd.open_workbook("3dMax.xls")
    table = date.sheets()[0]
    table = date.sheet_by_index(0)
    rows = table.nrows  # 行
    cols = table.ncols  # 列
    colnames = table.col_values(lie)  # 获取指定列的数据
    for items in colnames:
        list.append(items)
    return list


# 统计该概率最高的三个数
def getMaxNumber(number):
    ArrM = getExcelDate(number)
    return Counter(ArrM).most_common(3)


# 计算各个数字所占的百分比
def getEveryPercent(percent=[]):
    list = percent[1:len(percent)]
    labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    sizes = []
    for judex in labels:  # 各数字所占的百分比
        onePercent = list.count(judex) * 100.0 / len(percent)
        sizes.append(onePercent)
    return sizes


# 绘制饼状图
def drawPieView(arrM=[]):
    labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']  # 标题
    sizes = getEveryPercent(arrM)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax1.axis('equal')
    plt.show()


# 绘制直方图
def drawBarView():
    size = 10
    x = np.arange(size)
    a = getEveryPercent(getExcelDate(2))
    b = getEveryPercent(getExcelDate(3))
    c = getEveryPercent(getExcelDate(4))

    opacity = 0.8
    bar_width = 0.5


    plt.bar(x, a, width=bar_width/2,alpha=opacity,color='r',label=u'百位所占百分比')
    plt.bar(x + bar_width/2, b, width=bar_width/2,alpha=opacity,color='g', label=u'十位所占百分比')
    plt.bar(x + bar_width, c, width=bar_width/2,alpha=opacity,color='y', label=u'个位所占百分比')

    plt.xticks(x+bar_width-bar_width/4, ('1', '2', '3', '4', '5','6','7','8','9'))
    plt.yticks(fontsize=16) #标签文字大小
    plt.xticks(fontsize=16)

    plt.ylim(0, 12) #Y轴0-12
    plt.xlim(0, 9) #X轴0 - 9
    plt.xlabel(u'数字序列号')
    plt.ylabel(u'所占百分比')
    plt.title(u'3D福利彩票柱状图')
    # plt.legend()  #去掉标题
    plt.show()

    #折线图
def drawlineView():
    aY = getEveryPercent(getExcelDate(2))
    aX = range(0, 10)

    bY = getEveryPercent(getExcelDate(3))
    bX = range(0, 10)

    cY = getEveryPercent(getExcelDate(4))
    cX = range(0, 10)

    plt.plot(aX, aY, label=u'百位', linewidth=2.0, color='r', marker='o',
             markerfacecolor='w', markersize=5.0)
    plt.plot(bX, bY, label=u'十位',linewidth=2.0, color='g', marker='o',
             markerfacecolor='w', markersize=5.0)
    plt.plot(cX, cY, label=u'个位',linewidth=2.0, color='b', marker='o',
             markerfacecolor='w', markersize=5.0)

    plt.xlabel(u'期号')
    plt.ylabel(u'所占比例')
    plt.title(u'3D福利彩票所占比例')
    # plt.legend()
    plt.show()

if __name__ == '__main__':
    # 获取网页数据存入excel
    # creatExcel()
#     hunNUmber =  getMaxNumber(2)  #百位数字出现频率最高数据
#     tenNumber = getMaxNumber(3)  #十位出现最高频率的数据
#     singleNumber = getMaxNumber(4) #个位出现最高频率的数据
#     print(hunNUmber,tenNumber, singleNumber)
#
# # 圆饼图
#     allArrM = getExcelDate(3)        #得到百位所有的数据
#     drawPieView(allArrM)

# 绘制直方图
    drawBarView()


#折线图
    # drawlineView()
