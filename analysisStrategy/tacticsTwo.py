"""
作者：Lisongxi
公众号：上锁的安检门
描述：策略
"""
import pandas as pd

from dataCollection import capitalFlow


class StockForecast(object):
    def __init__(self, nowDate, estimate, actualValue):
        self.actualValue = actualValue
        self.estimate = estimate
        self.nowDate = nowDate


# 股票预测
def forcast():
    files = pd.read_csv(f'../data/1111.csv', skiprows=5)


if __name__ == "__main__":
    print("hello")
