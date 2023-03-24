import pandas as pd
import os
from math import floor, ceil

from main_functions import get_jsonparsed_data, estimated_time

apikey = os.environ.get("api_key")

def get_SP500():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp = pd.read_html(url)
    first_table = sp[0]
    second_table = sp[1]
    tickers = first_table["Symbol"]
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers  

def get_CAC40():
    url = "https://en.wikipedia.org/wiki/CAC_40"
    df = pd.read_html(url) 
    tickers = df[4]["Ticker"]
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers

def get_LSE():
    exchange_list = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={apikey}")
    tickers = []
    for symbol in exchange_list:
        if symbol[-2:] == ".L":
            tickers.append(symbol)
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers

def get_HKSE():
    # this one is weird because all stocks are numbers looks like nickname but balance sheets are available so ....
    exchange_list = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={apikey}")
    tickers = []
    for symbol in exchange_list:
        if symbol[-3:] == ".HK":
            tickers.append(symbol)
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers

def get_SHENZHEN():
    exchange_list = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={apikey}")
    tickers = []
    for symbol in exchange_list:
        if symbol[-3:] == ".SZ":
            tickers.append(symbol)
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers

def get_TKSE():
    exchange_list = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={apikey}")
    tickers = []
    for symbol in exchange_list:
        if symbol[-2:] == ".T":
            tickers.append(symbol)
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers

def get_SSE():
    exchange_list = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={apikey}")
    tickers = []
    for symbol in exchange_list:
        if symbol[-3:] == ".SS":
            tickers.append(symbol)
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers

def get_SET():
    # Bangkok stock exchange
    exchange_list = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={apikey}")
    tickers = []
    for symbol in exchange_list:
        if symbol[-3:] == ".BK":
            tickers.append(symbol)
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers 

def get_MCX():
    # Moscow stock exchange
    exchange_list = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={apikey}")
    tickers = []
    for symbol in exchange_list:
        if symbol[-3:] == ".ME":
            tickers.append(symbol)
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers 

def get_BME():
    # Bolsa De Madrid
    exchange_list = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={apikey}")
    tickers = []
    for symbol in exchange_list:
        if symbol[-3:] == ".MC":
            tickers.append(symbol)
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers 

def get_SGX():
    # Singapore stock exchange
    exchange_list = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={apikey}")
    tickers = []
    for symbol in exchange_list:
        if symbol[-3:] == ".SI":
            tickers.append(symbol)
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers

def get_JSX():
    # Jakarta stock exchange
    exchange_list = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={apikey}")
    tickers = []
    for symbol in exchange_list:
        if symbol[-3:] == ".JK":
            tickers.append(symbol)
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers

def faut_absolument_que_jappelle_Armand(limit = 10000):
    # Paris pour ceux qui doutent
    # A LOT OF DATAS FOR PARIS STOCK EXCHANGE ARE 1 YEAR LATE
    exchange_list = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=1&volumeMoreThan=1&exchange=euronext&limit={limit}&isEtf=False&isActivelyTrading=True&apikey={apikey}")
    tickers = []
    count = 0
    for key in exchange_list:
        if exchange_list[count]["exchange"] == "Paris":
            tickers.append(exchange_list[count]["symbol"])
        count +=1 
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers

def get_BMX():
    # Mexico stock exchange
    exchange_list = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey={apikey}")
    tickers = []
    for symbol in exchange_list:
        if symbol[-3:] == ".MX":
            tickers.append(symbol)
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers




# works for nyse, nasdaq, euronext, amex and tsx
def get_exchange(exchange: str, limit=10000):
    # you MUST put the limit parameter in the url and set it high otherwise you won't have all the stock !
    exchange_list = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan=1&volumeMoreThan=1&exchange={exchange}&limit={limit}&isEtf=False&isActivelyTrading=True&apikey={apikey}")
    tickers = []
    count = 0
    # get json parsed data return a list not a dict
    for key in exchange_list:
        symbol = exchange_list[count]["symbol"]
        tickers.append(symbol)
        count+=1
    print(f"Number of tickers {len(tickers)}")
    estimated_time(len(tickers))
    return tickers