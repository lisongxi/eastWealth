"""
作者：Lisongxi
公众号：上锁的安检门
描述：获取股票资金流
"""

import re
import time
import requests
import json
import pandas as pd
import stockData

# 传递参数
flowDatas = {
    "cb": "jQuery1123005287821234087975_" + str(int(time.time())),
    "po": 1,
    "pn": 1,
    "np": 1,
    "ut": "b2884a393a59ad64002292a3e90d46a5",
}

# 正则表达式
objLocation = re.compile(r"jQuery.*?\u0028(?P<dataJson>.*?)\u0029;", re.S)

# 链接
urls = "https://push2.eastmoney.com/api/qt/clist/get"


# 全部个股股票资金流（fid排序指标，可选f62今日主力净流入：净额）
def getAllStockCapitalFlow():
    flowDatas['fid'] = "f62"
    flowDatas['pz'] = 5000
    flowDatas['fltt'] = 2
    flowDatas['invt'] = 2
    flowDatas['fs'] = "m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2"
    flowDatas['fields'] = "f3,f12,f14,f62,f184,f66"
    column = ['今日涨跌幅', '股票编号', '股票名称', '今日主力净流入', '今日超大单净流入', '主力净占比']
    allStockCapitalFlow = requests.get(url=urls, params=flowDatas)
    result = json.loads(objLocation.findall(allStockCapitalFlow.text)[0])['data']['diff']

    return result, column


# 沪深A股资金流
def getHuShenCapitalFlow():
    flowDatas['fid'] = "f62"
    flowDatas['pz'] = 5000
    flowDatas['fltt'] = 2
    flowDatas['invt'] = 2
    flowDatas['fs'] = "m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2"
    flowDatas['fields'] = "f3,f12,f14,f62,f184,f66"
    column = ['今日涨跌幅', '股票编号', '股票名称', '今日主力净流入', '今日超大单净流入', '主力净占比']
    huShenCapitalFlow = requests.get(url=urls, params=flowDatas)
    result = json.loads(objLocation.findall(huShenCapitalFlow.text)[0])['data']['diff']

    return result, column


# 板块资金流（fid排序指标，可选f62今日主力净流入：净额）
def getblockCapitalFlow():
    flowDatas['fid'] = "f62"
    flowDatas['pz'] = 500
    # t:3是概念资金流
    flowDatas['fs'] = "m:90+t:2"
    flowDatas['fields'] = "f12,f14,f3,f62,f184,f66,f204"
    flowDatas['_'] = str(int(time.time()))
    column = ['今日涨跌幅', '板块编号', '板块名称', '今日主力净流入', '今日超大单净流入', '主力净占比',
              '主力净流入最大股', '最大股代码', '-']
    blockCapitalFlow = requests.get(url=urls, params=flowDatas)
    result = json.loads(objLocation.findall(blockCapitalFlow.text)[0])['data']['diff']

    return result, column


# 主力资金流
def getMainForceCapitalFlow():
    flowDatas['fid'] = "f184"
    flowDatas['pz'] = 5000
    flowDatas['fltt'] = 2
    flowDatas['invt'] = 2
    flowDatas['fs'] = "m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2"
    flowDatas['fields'] = "f2,f3,f12,f14,f62,f100,f109,f184"
    column = ['最新价', '5日涨跌幅', '股票代码', '股票名称', '主力净流入', '所属板块', '10日涨跌', '主力净占比']
    MainForceCapitalFlow = requests.get(url=urls, params=flowDatas)
    result = json.loads(objLocation.findall(MainForceCapitalFlow.text)[0])['data']['diff']

    return result, column


# 个股历史资金流
def getStockHistoryCapitalFlow(stockCode):
    datas = {
        "cb": "jQuery1123006321496735543075_" + str(int(time.time())),
        "lmt": "0",
        "klt": "101",
        "fields1": "f1,f2,f3,f7",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61,f62,f63,f64,f65",
        "ut": "b2884a393a59ad64002292a3e90d46a5",
        "secid": stockData.getSecid(stockCode),
        "_": str(int(time.time()))
    }
    urll = "https://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get"
    stockHistoryCapitalFlow = requests.get(url=urll, params=datas)

    result = json.loads(objLocation.findall(stockHistoryCapitalFlow.text)[0])['data']['klines']

    results = []
    for xxx in result:
        ppp = xxx.split(",")
        results.append(ppp)

    column = ['日期', '主力净流入:净额', '小单净流入:净额', '中单净流入:净额', '大单净流入:净额', '超大单净流入:净额',
              '主力净占比', '小单净占比', '中单净占比', '大单净占比', '超大单净占比', '收盘价', '涨跌幅', '-', '-']
    return results, column


if __name__ == "__main__":

    # 自行修改想要运行哪个函数
    result, column = getMainForceCapitalFlow()
    df = pd.DataFrame(result)
    df.columns = column

    # 结果写入，根据自己需要修改结果名称
    df.to_csv(f'../data/主力资金流.csv', index=False)
