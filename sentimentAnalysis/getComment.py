"""
作者：Lisongxi
公众号：上锁的安检门
描述：获取股票评论
"""

import requests
from bs4 import BeautifulSoup
import xlsxwriter
import time

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}


def getStockComment(stockCode):
    workbook = xlsxwriter.Workbook('../data/result.xlsx')  # 创建一个excel文件

    # 创建工作表
    worksheet = workbook.add_worksheet()

    # 写入数据
    worksheet.write(0, 0, 'time')  # 第1行第1列（即A1）写入
    worksheet.write(0, 1, 'comment')

    # 记录excel行数
    i = 1

    # 获取20页评论（可手动修改页数）
    for page in range(1, 20):
        # 评论链接
        commentUrl = "http://guba.eastmoney.com/list,%s_%s.html" % (stockCode, page)

        commentResp = requests.get(url=commentUrl, headers=header)

        pageComment = BeautifulSoup(commentResp.text, 'html.parser')

        # 从第1个开始获取，第0个不要了
        comments = pageComment.find_all("div", class_="articleh normal_post")[1:]

        for comment in comments:
            comm = comment.find("a").text
            times = "2023-" + comment.find("span", class_="l5 a5").text
            comm_time = time.strftime("%Y/%m/%d %H:%M", time.strptime(times, "%Y-%m-%d %H:%M"))
            # 写入excel文件
            worksheet.write(i, 0, comm_time)
            worksheet.write(i, 1, comm)
            i += 1

    # 关闭保存excel文件
    workbook.close()
    print("获取评论完成")


if __name__ == "__main__":
    getStockComment("002261")
