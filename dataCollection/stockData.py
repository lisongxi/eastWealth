"""
作者：Lisongxi
公众号：上锁的安检门
描述：获取沪京深A股数据
"""
import json
import re
import time
import requests


# 获取获取沪京深所有A股数据
def getAllStockData(fid):
    urls = "http://75.push2.eastmoney.com/api/qt/clist/get"

    datas = {
        "cb": "jQuery11240656050521505366_" + str(int(time.time())),
        "pn": 1,
        "pz": 5320,
        "po": 1,
        "np": 1,
        "ut": "bd1d9ddb04089700cf9c27f6f7426281",
        "fltt": 2,
        "invt": 2,
        "wbp2u": "|0|0|0|web",
        "fid": fid,
        "fs": "m:0 t:6,m:0 t:80,m:1 t:2,m:1 t:23,m:0 t:81 s:2048",
        "fields": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152",
        "_": str(int(time.time()))
    }

    res = requests.get(url=urls, params=datas)

    objLocation = re.compile(r"jQuery.*?\u0028(?P<dataJson>.*?)\u0029;", re.S)
    results = json.loads(objLocation.findall(res.text)[0])

    return results


# 获取某个股票的K线图全部数据
def getKlineData(stockCode):
    klineUrl = "http://75.push2his.eastmoney.com/api/qt/stock/kline/get"

    # fields:返回的参数，可根据自行需要填写。
    param = {
        "cb": "jQuery35106426223250373209_" + str(int(time.time())),
        "secid": getSecid(stockCode),
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": "101",  # k线间距 默认为 101 即日k
        "fqt": "1",
        "end": "20500101",
        "lmt": "5000",
        "_": str(int(time.time()))
    }

    klineResp = requests.get(url=klineUrl, params=param)

    objLocation = re.compile(r"jQuery.*?\u0028(?P<dataJson>.*?)\u0029;", re.S)
    results = json.loads(objLocation.findall(klineResp.text)[0])

    return results


def getSecid(stockcode: str) -> str:
    '''
    生成东方财富专用的secid
    Parameters
    ----------
    stockcode : 6 位股票代码
    Return
    ------
    str: 指定格式的字符串
    '''
    # 沪市指数
    if stockcode[:3] == '000':
        return f'0.{stockcode}'
    # 深证指数
    if stockcode[:3] == '399':
        return f'0.{stockcode}'

    if stockcode[0] != '6':
        return f'0.{stockcode}'

    return f'1.{stockcode}'


if __name__ == "__main__":
    # 修改fid值，可以输出不同的排序方式。当前以 f20总市值 进行排序。
    results = getAllStockData("f20")

    with open("../data/allStockData.json", "w") as f:
        json.dump(results, f)

    # print(getKlineData('000333'))

    '''参数解释：
        'f51': '日期',
        'f52': '开盘',
        'f53': '收盘',
        'f54': '最高',
        'f55': '最低',
        'f56': '成交量',
        'f57': '成交额',
        'f58': '振幅',
        'f59': '涨跌幅',
        'f60': '涨跌额',
        'f61': '换手率',

    '''
