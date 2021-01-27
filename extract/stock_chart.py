from api import *
import math
import pandas as pd
from extract.market_stock import MarketTotal

def reverse(classtype):
    return dict((value, key) for key, value in classtype.__dict__)

class StockChartInput:
    stock_code = 0
    req_type = 1 # '1': 기간(하루) / '2': 갯수
    end_date = 2
    start_date = 3
    count = 4
    field = 5 #
    type = 6
    freq = 7
    adjusted = 9
    volume = 10

class StockChartHeader:
    stock_code = 0
    field_count = 1
    field_array = 2
    received_count = 3
    volume = 10
    ask = 11
    bid = 12
    open = 13
    high = 14
    low = 15
    transaction = 16
    listed_stock = 17

class StockChartField:
    date = 0
    time = 1
    open = 2
    high = 3
    low = 4
    close = 5
    volume = 8
    transaction = 9
    listed_stock =12
    market_cap = 13


class StockData(CREON):

    max_count = 99999
    def __init__(self):
        # freq : D / m = 1,3,5,..
        super().__init__()
        self.objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
        self.count = None

    def get_date_data(self, code, data_freq="D", start_date=None, end_date=None, adjusted = True, columns=[]): # limit: 6665

        self.objStockChart.SetInputValue(StockChartInput.stock_code, code)  # 종목코드
        if start_date:
            self.objStockChart.SetInputValue(StockChartInput.req_type, ord('1'))  # '1': 기간
            self.objStockChart.SetInputValue(StockChartInput.start_date, start_date)  # To 날짜
            self.objStockChart.SetInputValue(StockChartInput.end_date, end_date)  # From 날짜
        columns.insert(0, "date")
        if len(data_freq) > 1:
            columns.insert(1, "time")
            freq, data_freq  = int(data_freq[0]), data_freq[1].lower()
            assert data_freq == 'm'
            self.objStockChart.SetInputValue(StockChartInput.type, ord(data_freq))
            self.objStockChart.SetInputValue(StockChartInput.freq, freq)
        else:
            assert data_freq in ['D', 'W', 'M']
            self.objStockChart.SetInputValue(StockChartInput.type, ord(data_freq))
        data = [getattr(StockChartField, i) for i in columns]
        self.objStockChart.SetInputValue(StockChartInput.field, data)
        if adjusted:
            self.objStockChart.SetInputValue(StockChartInput.adjusted, ord('1'))  # 수정주가 사용
        self.columns = columns
        return self.receive_data()

    def get_minute_data(self, code, minute, dates=None, adjusted = True, columns=[]):

        self.count = math.ceil(381/minute)
        if dates is not None:
            self.count *= dates
        self.objStockChart.SetInputValue(StockChartInput.stock_code, code)  # 종목코드
        self.objStockChart.SetInputValue(StockChartInput.req_type, ord('2'))
        self.objStockChart.SetInputValue(StockChartInput.count, self.count)  # 조회 개수
        columns.insert(0, "date")
        columns.insert(1, "time")
        data = [getattr(StockChartField, i) for i in columns]
        print(data)
        self.objStockChart.SetInputValue(StockChartInput.field, data)
        self.objStockChart.SetInputValue(StockChartInput.type, ord("m"))
        self.objStockChart.SetInputValue(StockChartInput.freq, minute)
        if adjusted:
            self.objStockChart.SetInputValue(StockChartInput.adjusted, ord('1'))  # 수정주가 사용
        self.columns = columns
        return self.receive_data()

    def get_tick_data(self, code, tick, adjusted=True): # 종가 데이터

        self.count = self.max_count
        self.objStockChart.SetInputValue(StockChartInput.stock_code, code)  # 종목코드
        self.objStockChart.SetInputValue(StockChartInput.req_type, ord('2'))  # '1': 기간
        self.objStockChart.SetInputValue(StockChartInput.count, self.count)  # 조회 개수
        columns = ["date",  "time" , "close"]
        data = [getattr(StockChartField, i) for i in columns]
        self.objStockChart.SetInputValue(StockChartInput.field, data)
        self.objStockChart.SetInputValue(StockChartInput.type, ord("T"))
        self.objStockChart.SetInputValue(StockChartInput.freq, tick)
        if adjusted:
            self.objStockChart.SetInputValue(StockChartInput.adjusted, ord('1'))  # 수정주가 사용
        return self.receive_data()


    def check_request(self):
        self.objStockChart.BlockRequest()
        rqStatus = self.objStockChart.GetDibStatus()
        if rqStatus != 0:
            return False
        self.count = self.objStockChart.GetHeaderValue(StockChartHeader.received_count)
        if self.count <= 1:
            return False
        return int(self.count)

    def receive_data(self):
        result = {col : [] for col in self.columns}
        total_received = 0
        while True:
            self.check_remain_time()
            received = self.check_request()
            total_received += received
            if received and (isinstance(self.count, int) and self.count >= total_received):
                print(f"start to receive : {received*len(self.columns)}")
                for i in range(received):
                    for idx, col in enumerate(self.columns):
                        result[col].append(self.objStockChart.GetDataValue(idx, i))
            else:
                break
        result = pd.DataFrame(result)
        if 'date' in result.columns and 'time' in result.columns:
            result['date'] = result['date'].astype('str')
            result['time'] = result['time'].astype('str')
            result.sort_values(by=['date', 'time'], inplace=True)
        elif 'date' in result.columns:
            result['date'] = result['date'].astype('str')
            result.sort_values(by=['date'], inplace=True)

        return result


if __name__ == "__main__":

    sample = "A005930"
    data = StockData()
    print(data.get_minute_data(code = sample, minute=1, columns = ['open', 'close', 'high', 'low']))
