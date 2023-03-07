import datetime as dt
import pandas as pd
import os, sys
from dotenv import load_dotenv
import time
import certifi
import json
import math, statistics, numpy as np, seaborn as sns


try:
    from urllib.request import urlopen
except(ImportError):
   sys.exit("Can't import urlllib") 

load_dotenv()
apikey = os.environ.get("api_key")

if apikey == None:
    sys.exit("No APIKEY")

class market_data:
    pass
    def __init__(self, name, year):
        self.name = name
        self.year = year
    
    def market_mean(values):
        return statistics.mean(values)

class stock:
    pass

def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


def get_SP500_list():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp = pd.read_html(url)
    first_table = sp[0]
    second_table = sp[1]
    tickers = first_table["Symbol"]
    return tickers   

def api_call(symbol):
    global timer_function_start
    timer_function_start = time.perf_counter()
    count = 0
    for attemps in range(4):
        # check for errors
        try:
            # add enterprise value / ebitda and enterprise value / free cash flow both are in keyMetricsTTM
            financialRatios = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={apikey}")
            #scores = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v4/score?symbol={symbol}&apikey={apikey}")
            keyMetrics = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{symbol}?apikey={apikey}")
            stockQuote = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={apikey}")
            discountedCashFlow = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v4/advanced_levered_discounted_cash_flow?symbol={symbol}&apikey={apikey}")
            print(f"FOUND TICKER: {symbol}")
            break
        except:
            count += 1
            if count == 4:
                print("Can't find this ticker, will pass")
                break
            print(f"{count} attempts, can't find this ticker, trying again")
            continue
    return stockQuote, financialRatios, keyMetrics, discountedCashFlow

def get_datas(list_of_symbols):
    #declare the dictionnaries which will store the different data
    price, returnOnEquityTTM, priceEarningsRatioTTM, grahamNumberTTM, enterpriseValueTTM, \
        returnOnInvestedCapitalTTM, enterpriseValueOverEBITDATTM, enterpriseValueOverFreeCashFlowTTM = \
          ({} for i in range(8))
    meanReturnOnEquityTTM, meanPriceEarningsRatioTTM, meanReturnOnInvestedCapitalTTM = ([] for i in range(3))
    counter = 0
    for symbol in list_of_symbols:
        # make the api calls
        stockQuote, financialRatios, keyMetrics, discountedCashFlow  = api_call(symbol)
        # retrieve the price and display it
        current_price = stockQuote[0]["price"]
        price[symbol] = current_price
        print(f"Price is {current_price}")
        # retrieve the different datas we are interested in
        retrieve_datas(financialRatios, "returnOnEquityTTM", symbol, returnOnEquityTTM, meanReturnOnEquityTTM)
        retrieve_datas(financialRatios, "priceEarningsRatioTTM", symbol, priceEarningsRatioTTM, meanPriceEarningsRatioTTM)
        retrieve_datas(financialRatios, "returnOnCapitalEmployedTTM", symbol, returnOnInvestedCapitalTTM, meanReturnOnInvestedCapitalTTM)
        retrieve_datas(keyMetrics, "grahamNumberTTM", symbol, grahamNumberTTM)
        retrieve_datas(keyMetrics, "enterpriseValueTTM", symbol, enterpriseValueTTM)
        retrieve_datas(keyMetrics, "enterpriseValueOverEBITDATTM", symbol, enterpriseValueOverEBITDATTM)
        retrieve_datas(keyMetrics, "evToFreeCashFlowTTM", symbol, enterpriseValueOverFreeCashFlowTTM)
        counter += 1
        print(f"{counter} ticker(s) retrieved")
        if counter == 5:
            break
        timer_function_end = time.perf_counter()
        print(f"Time elapsed to retrive this ticker : {timer_function_end - timer_function_start}")
        means_dict = {"roeMean" : meanReturnOnEquityTTM, "perMean" : meanPriceEarningsRatioTTM, "roicMean" : meanReturnOnInvestedCapitalTTM}
    return price, returnOnEquityTTM, priceEarningsRatioTTM, grahamNumberTTM, enterpriseValueTTM, returnOnInvestedCapitalTTM, \
    enterpriseValueOverEBITDATTM, enterpriseValueOverFreeCashFlowTTM, means_dict


def sorting_dict_values(dic):
    sorted_dic = {key : value for key, value in sorted(dic.items(), key=lambda value : value[1], reverse=False)}
    return sorted_dic

def sorting_dict_values_reversed(dic):
    sorted_dic = {key : value for key, value in sorted(dic.items(), key=lambda value : value[1], reverse=True)}
    return sorted_dic  

def sorting_nested_dict_values(dic):
    sorted_dic = sorted(dic.items(), key=lambda value : value[1]["roe"])
    return sorted_dic

def dic_to_CSV(dic, name):
    current_directory = os.getcwd()
    path = f"{current_directory}/CSV"
    df = pd.DataFrame.from_dict(dic, orient="index")
    df.to_csv(f"{path}/{name}.csv", index=True, header=True)
    return

def retrieve_datas(bulk_datas, specific_data, symbol, name_of_the_dict, mean_array = None):
    if not bulk_datas or bulk_datas[0][f"{specific_data}"] == None:
        print(f"{specific_data} no found")
    else:
        name_of_the_dict[symbol] = bulk_datas[0][f"{specific_data}"]
        print(f"Found {specific_data}")
        if(mean_array != None):
            mean_array.append(bulk_datas[0][f"{specific_data}"])

#clean data for mean calculation
def data_cleaning(array):
    # need to improve this in the future since it removes too much value on the upper bound i think
    median = np.median(array)
    q1 = np.quantile(array, 0.25)
    q3 = np.quantile(array, 0.75)
    iqr = q3 - q1
    # the widely accepted constant for this type of outliers is 1.5 but in our case it's too small
    upper_bound_outlier = q3 + 2.25*(iqr)
    lower_bound_outlier = q1 - 2.25*(iqr)
    l, r = 0, len(array)-1
    while(True):
        if array[l] > lower_bound_outlier and array[r] < upper_bound_outlier:
            # stop if all values are in the range
            break
        elif array[l] < lower_bound_outlier:
            # if the value is out of bound remove it and remove one from the other side too to balance it
            array.pop(0)
            array.pop()
        elif array[r] > upper_bound_outlier:
            # same for upper bound
            array.pop()
            array.pop(0)
    print(median, q1, q3, upper_bound_outlier, lower_bound_outlier)
    return array


def calculate_means(dict_datas_of_symbols):
    # the argument passed is a dict with the corresponding key and data for example dict["roeMean"] contain an array with all the roe retrieved
    # so we can apply the mean operations
    # maybe check the type of the datas e.g dict or array to adapt
    for key in dict_datas_of_symbols:
        if dict_datas_of_symbols[key]: 
            dict_datas_of_symbols[key] = statistics.mean(dict_datas_of_symbols[key]) 