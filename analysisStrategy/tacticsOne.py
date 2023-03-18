"""
作者：Lisongxi
公众号：上锁的安检门
描述：策略
"""
import json

import pandas as pd

from dataCollection import stockData


class StockRank(object):
    def __init__(self, stockName, stockCode, stockScore, marketValue):
        self.stockCode = stockCode
        self.stockName = stockName
        self.stockScore = stockScore
        self.marketValue = marketValue


def findByUpDown():
    """
    1）查找前300个交易日跌幅较多和最近10个交易日涨幅较多的股票的综合得分
    2）排位越靠前，代表 前300个交易日跌幅较多，最近10个交易日涨幅较多
    3）排位越靠后，代表 前300个交易日跌幅较少，最近10个交易日涨幅较少

    注意：
    1）仅根据部分数据得出结论，不构成投资意见
    2）仅仅是随便做的排序，不构成投资意见
    :return:
    """

    # 等级列表
    rankList = []

    # 读取本地json文件
    # with open("./data/allStockData.json", "r", encoding="utf-8") as f:
    #     stockDataSet = json.load(f)['data']['diff']

    # 实时获取数据
    stockDataSet = stockData.getAllStockData("f20")['data']['diff']

    for stocks in stockDataSet:

        klines = stockData.getKlineData(stocks['f12'])['data']['klines']

        # 跳过退市股票
        if not klines or "退" in stocks['f14'] or stocks['f20'] == "-":
            continue

        print("开始处理：" + stocks['f12'])

        date1_data = klines[max(len(klines) - 300, 0)].split(',')
        date2_data = klines[max(len(klines) - 10, 0)].split(',')
        date3_data = klines[len(klines) - 1].split(',')

        # 前300个交易日跌幅、最近10个交易日涨幅
        score1 = ((float(date1_data[2]) - float(date2_data[2])) / abs(float(date1_data[2]))) * 50
        score2 = ((float(date3_data[2]) - float(date2_data[2])) / abs(float(date2_data[2]))) * 50
        score = score2 + score1

        # 总市值
        marketValue = round(stocks['f20'] / 100000000, 2)

        stock = StockRank(stocks['f14'], stocks['f12'], score, marketValue)

        rankList.append(stock)

    # 根据得分排序
    result = sorted(rankList, key=lambda s: s.stockScore, reverse=True)

    # 将列表转换为 DataFrame
    df = pd.DataFrame([vars(rs) for rs in result])
    df.columns = ['股票代码', '名称', '得分', '总市值(亿)']

    # 将 DataFrame 写入 CSV 文件
    df.to_csv("./data/findByUpDown.csv", index=False)


def findByMarketValue():
    """
        1）查找前100个交易日跌幅和总市值相乘，结果最大的股票
        2）即查找近100个交易日跌幅最大，但是总市值也较高的股票

        注意：
        1）仅根据部分数据得出结论，不构成投资意见
        2）仅仅是随便做的排序，不构成投资意见
        3）A股跟政策有非常大的关系，并非数据随随便便就能预测
        :return:
        """

    # 等级列表
    rankList = []

    # 读取本地json文件
    # with open("./data/allStockData.json", "r", encoding="utf-8") as f:
    #     stockDataSet = json.load(f)['data']['diff']

    stockDataSet = stockData.getAllStockData("f20")['data']['diff']

    for stocks in stockDataSet:

        klines = stockData.getKlineData(stocks['f12'])['data']['klines']

        # 跳过退市股票
        if not klines or "退" in stocks['f14'] or stocks['f20'] == "-":
            continue

        print("开始处理：" + stocks['f12'], end="  ")

        date1_data = klines[max(len(klines) - 100, 0)].split(',')
        date2_data = klines[len(klines) - 1].split(',')

        # 总市值
        marketValue = round(stocks['f20'] / 100000000, 2)

        # 前100个交易日
        score = ((float(date1_data[2]) - float(date2_data[2])) / abs(float(date1_data[2]))) * marketValue
        print("日期：" + date1_data[0])

        stock = StockRank(stocks['f14'], stocks['f12'], score, marketValue)

        rankList.append(stock)

    # 根据得分排序
    result = sorted(rankList, key=lambda s: s.stockScore, reverse=True)

    # 将列表转换为 DataFrame
    df = pd.DataFrame([vars(rs) for rs in result])
    df.columns = ['股票代码', '名称', '得分', '总市值（亿）']

    # 将 DataFrame 写入 CSV 文件
    df.to_csv("./data/findByMarketValue.csv", index=False)


if __name__ == "__main__":
    # 注意，如果从此文件运行，则需要更改 ./data 为 ../data ,从main文件运行则不用改
    # 其实用绝对路径就没有这种烦恼了

    findByUpDown()
    # findByMarketValue()
