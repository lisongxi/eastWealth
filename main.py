"""
作者：Lisongxi
公众号：上锁的安检门
描述：获取东方财富的股票信息。本程序目的是通过数据做一些自己想要的策略，如果仅仅是想看股票排行榜之类的，直接上东方财富更便捷。
"""
from analysisStrategy import tacticsOne

if __name__ == '__main__':
    print('Hello 东财 爬你')

    # 策略一：查找前300个交易日跌幅较多和最近10个交易日涨幅较多的股票的综合得分
    tacticsOne.findByUpDown()

    # 策略二：查找近100个交易日跌幅最大，总市值较高的股票
    # tacticsOne.findByMarketValue()
