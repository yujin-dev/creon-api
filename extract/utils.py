from api import *

def get_stock_code(name):
    return g_objStockMgr.NameToCode(name)

if __name__ == "__main__":
    print(get_stock_code("하나기술"))