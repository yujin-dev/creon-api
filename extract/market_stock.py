from api import *
import pandas as pd

class MarketTotalField:
    stock_code = 0
    time = 1
    trend = 2
    current = 4
    open = 5
    high = 6
    low = 7
    ask = 8
    bid = 9
    volume = 10
    transaction = 11
    listed_stock = 20


class MarketTotal:

    def __init__(self):
        self.objRq = win32com.client.Dispatch("CpSysDib.MarketEye")

    def get_stock_list(self, stock_type='all'):

        if stock_type=='all':
            kospi = g_objCodeMgr.GetStockListByMarket(1)  # 코스피
            kosdaq = g_objCodeMgr.GetStockListByMarket(2)  # 코스닥
        elif stock_type=='kospi':
            kospi = g_objCodeMgr.GetStockListByMarket(1)  # 코스피
            kosdaq = ()
        elif stock_type=='kosdaq':
            kospi = ()  # 거래소
            kosdaq = g_objCodeMgr.GetStockListByMarket(2)  # 코스닥
        else:
            raise Exception(f"{stock_type} is not properly set")
        stock_list = kospi + kosdaq  # tuple
        return stock_list

    def request_market_cap(self, stock_codes, data_info = {}):

        self.columns = [MarketTotalField.stock_code, MarketTotalField.current, MarketTotalField.listed_stock]
        self.objRq.SetInputValue(0, self.columns)
        self.objRq.SetInputValue(1, stock_codes)
        self.objRq.BlockRequest()

        rqStatus = self.objRq.GetDibStatus()
        if rqStatus != 0:
            return False
        cnt = self.objRq.GetHeaderValue(2) # 종목 갯수

        for i in range(cnt):
            code = self.objRq.GetDataValue(self.columns[0], i)
            cur = self.objRq.GetDataValue(1, i)
            listedStock = self.objRq.GetDataValue(2, i)
            market_cap = listedStock * cur

            if g_objCodeMgr.IsBigListingStock(code):
                market_cap *= 1000
            data_info[code] = market_cap
        return True

    def get_stock_marketcap(self, stock_type):
        stock_list = self.get_stock_list(stock_type)
        split_list = [stock_list[i: i+200] for i in range(0, len(stock_list), 200)]

        self.result = {}
        for codes in split_list:
            self.request_market_cap(codes, self.result)
        return pd.DataFrame(self.result)


if __name__ == "__main__":

    sample = "kosdaq"
    market = MarketTotal()
    print(market.get_stock_marketcap(sample))
