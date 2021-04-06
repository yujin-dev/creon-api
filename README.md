# CREON-DATA-LOADER

CREON PLUS API를 이용한 데이터 DB 저장 및 활용

## usage
- market_type에 따른 시장 종목정보
 ```python
market = MarketTotal()
market_data = market.get_stock_marketcap("kosdaq")
```

- 분 데이터 예시
```python
data = StockData()
minute_data = data.get_minute_data(code = "A005930", minute=1, columns = ['open', 'close', 'high', 'low'])
```

- candlestick 데이터 graph를 위한 requirements

``` $pip install https://github.com/matplotlib/mpl_finance/archive/master.zip```

