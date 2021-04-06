from extract.stock_chart import *
from extract.market_stock import *
import pandas as pd
from config import *

class DataLoader:

    def __init__(self):
        self.engine = engine

    def update(self, table, data):
        data.to_sql(table, con=self.engine, if_exists="append", index=False)

    def _source(self):
        self.data_source = StockData()
        self.market = MarketTotal()

    def store_minute_data(self, market_type="kosdaq", minute=1):

        self._source()
        all_stock = self.market.get_stock_list(market_type)

        for code in all_stock:
            data = self.data_source.get_minute_data(code=code, minute=minute, columns=['open', 'close', 'high', 'low', 'volume'])
            data['stock_code'] = code
            self.update('minute_data', data)

    def store_tick_data(self, market_type="kosdaq", tick=1):

        self._source()
        all_stock = self.market.get_stock_list(market_type)

        for code in all_stock:
            data = self.data_source.get_tick_data(code=code, tick=tick)
            data['stock_code'] = code
            self.update('tick_data', data)

    def store_minute_transation(self, market_type="kosdaq", minute=1):

        self._source()
        all_stock = self.market.get_stock_list(market_type)

        for code in all_stock:
            data = self.data_source.get_minute_data(code=code, minute=minute, columns=['transaction'])
            data['stock_code'] = code
            self.update('minute_transaction', data)

class SearchData(DataLoader):

    def __init__(self):
        super().__init__()

    def get_specific_data(self, table, date=None, stock_code=None):
        sql = f"""
        SELECT * FROM {table}"""
        cons = []
        if date is not None:
            cons.append(f"date={date}")
        if stock_code is not None:
            cons.append(f"stock_code={stock_code}")
        if len(cons)>0:
            sql += "WHERE"
            sql += " and ".join(cons)
        result = pd.read_sql(sql, con = self.engine)
        return result

if __name__ == "__main__":

    loader = DataLoader()
    loader.store_minute_data(market_type="kosdaq", minute=1)