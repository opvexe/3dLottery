#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# -*- author:SHUMIN -*-

import urllib2
import urllib
import re
import xlwt
import xlrd
from collections import Counter
import matplotlib.pyplot as plt #绘制折线

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

#正则法则匹配对应的数据
def reGetHtml():
    temp = getWebUrl()
    reg = re.compile(r'<tr>.*?<td align="center">'
                     r'(.*?)</td>.*?<td align="center">'
                     r'(.*?)</td>.*?<td align="center" '
                     r'style="padding-left:20px;">'
                     r'<em>(.*?)</em>.*?<em>(.*?)</em>.*?'
                     r'<em>(.*?)</em></td>', re.S)
    reScouce = re.findall(reg, temp)
    return  reScouce


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

#绘制折线
# def drawChartView(chart):
#
#    list  = []
#    for item in range(1,len(chart)):
#        list.append(chart[item])
#
#     plt.plot(list)
#     plt.show()

if __name__ == '__main__':
   #  获取网页数据存入excel
   # creatExcel()
   hunNUmber =  getMaxNumber(2)  #百位数字出现频率最高数据
   tenNumber = getMaxNumber(3)  #十位出现最高频率的数据
   singleNumber = getMaxNumber(4) #个位出现最高频率的数据
   print(hunNUmber,tenNumber, singleNumber)

   #绘制图形
   # drawChartView(getExcelDate(2))
