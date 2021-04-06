from config import *
import pandas as pd
import matplotlib.pyplot as plt
from extract.stock_chart import *
from extract.utils import *
from analysis.candlestick import draw_candlestick
from analysis.utils import *

class Filter(StockData, MarketTotal):
    def __init__(self, target, start_date=None, end_date=None):
        super().__init__()
        if target in ['all', 'kospi', 'kosdaq']:
            self.target = self.get_stock_list(target)
        elif target.startswith('A'):
            self.target = target
        else:
            self.target = get_stock_code(target)
        # self.source = StockData()
        self.start_date = start_date
        self.end_date = end_date
    def check1(self): # 거래대금 50억이상

        total = pd.DataFrame()
        if isinstance(self.target, list) or isinstance(self.target, tuple):
            for t in self.target:
                result = self.get_date_data(code=t, data_freq="5m", start_date=self.start_date, end_date=self.end_date, columns=["transaction"])
                result['stock_code'] = [t for _ in range(len(result))]
                total = pd.concat([result, total])
                print(len(total))

        self.filtered = total[total['transaction']>=5000000000]
        print(self.filtered)

    def check2(self): # 가격 10% 이상
        pass

    def check3(self):
        filtered_code = self.filtered['stock_code'].unique()
        total = pd.DataFrame()
        if isinstance(filtered_code, list) or isinstance(filtered_code, tuple):
            for t in filtered_code:
                result = self.get_date_data(code=t, data_freq="1m", start_date=self.start_date, end_date=self.end_date, columns=["open", "close", "volume"])
                result['stock_code'] = [t for _ in range(len(result))]
                total = pd.concat([result, total])
                print(len(total))


    def run(self):
        self.check1()
        self.check2()
        self.check3()

if __name__ == "__main__":
    Filter('kosdaq', 20210118, 20210119).run()