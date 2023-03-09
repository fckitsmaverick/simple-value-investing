import datetime as dt
import pandas as pd
import os, sys
from dotenv import load_dotenv
import time
import certifi
import json
import math, statistics, numpy as np, seaborn as sns, matplotlib.pyplot as plt


try:
    from urllib.request import urlopen
except(ImportError):
   sys.exit("Can't import urlllib") 

load_dotenv()
apikey = os.environ.get("api_key")

if apikey == None:
    sys.exit("No APIKEY")


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
    symbol = symbol.replace(".", "-")
    for attemps in range(4):
        # check for errors
        try:
            # add enterprise value / ebitda and enterprise value / free cash flow both are in keyMetricsTTM
            financialRatiosTTM = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={apikey}")
            #scores = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v4/score?symbol={symbol}&apikey={apikey}")
            keyMetricsTTM = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{symbol}?apikey={apikey}")
            stockQuoteTTM = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={apikey}")
            discountedCashFlowTTM = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v4/advanced_levered_discounted_cash_flow?symbol={symbol}&apikey={apikey}")
            print(f"FOUND TICKER: {symbol}")
            break
        except:
            count += 1
            if count == 5:
                print("Can't find this ticker, will pass")
                break
            print(f"{count} attempts, can't find this ticker, trying again")
            continue
    return stockQuoteTTM, financialRatiosTTM, keyMetricsTTM, discountedCashFlowTTM


def stock_api_call(symbol):
    count = 0
    for attempts in range(4):
        try:
            financialStatement = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/income-statement/{symbol}?limit=120&apikey={apikey}")
            keyMetrics = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?limit=40&apikey={apikey}")
            stockQuote = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/quote-short/{symbol}?apikey={apikey}")
        except:
            count += 1
            if count == 5000:
                print("Can't find this ticker")
                break
            print(f"{count} attempts, can't find this ticker, trying again")
    return financialStatement, keyMetrics, stockQuote

def get_datasTTM(list_of_symbols):
    # will problably have to change this function it's too messy
    #declare the dictionnaries which will store the different data
    price, bulk_datas, returnOnEquityTTM, priceEarningsRatioTTM, grahamNumberTTM, enterpriseValueTTM, \
        returnOnInvestedCapitalTTM, enterpriseValueOverEBITDATTM, enterpriseValueOverFreeCashFlowTTM = \
          ({} for i in range(9))
    meanReturnOnEquityTTM, meanPriceEarningsRatioTTM, meanReturnOnInvestedCapitalTTM = ([] for i in range(3))
    counter = 0
    for symbol in list_of_symbols:
        # make the api calls
        stockQuote, financialRatios, keyMetrics, discountedCashFlow  = api_call(symbol)
        # retrieve the different datas we are interested in
        retrieve_datasTTM(stockQuote, "price", symbol, price, bulk_datas)
        retrieve_datasTTM(financialRatios, "returnOnEquityTTM", symbol, returnOnEquityTTM, bulk_datas, meanReturnOnEquityTTM)
        retrieve_datasTTM(financialRatios, "priceEarningsRatioTTM", symbol, priceEarningsRatioTTM, bulk_datas, meanPriceEarningsRatioTTM)
        retrieve_datasTTM(financialRatios, "returnOnCapitalEmployedTTM", symbol, returnOnInvestedCapitalTTM, bulk_datas, meanReturnOnInvestedCapitalTTM)
        retrieve_datasTTM(keyMetrics, "grahamNumberTTM", symbol, grahamNumberTTM, bulk_datas)
        retrieve_datasTTM(keyMetrics, "enterpriseValueTTM", symbol, enterpriseValueTTM, bulk_datas)
        retrieve_datasTTM(keyMetrics, "enterpriseValueOverEBITDATTM", symbol, enterpriseValueOverEBITDATTM, bulk_datas)
        retrieve_datasTTM(keyMetrics, "evToFreeCashFlowTTM", symbol, enterpriseValueOverFreeCashFlowTTM, bulk_datas)
        counter += 1
        print(f"{counter} ticker(s) retrieved")
        if counter == 5000:
            break
        timer_function_end = time.perf_counter()
        print(f"Time elapsed to retrive this ticker : {timer_function_end - timer_function_start}")
        means_dict = {"roeMean" : meanReturnOnEquityTTM, "perMean" : meanPriceEarningsRatioTTM, "roicMean" : meanReturnOnInvestedCapitalTTM}
    return price, bulk_datas, returnOnEquityTTM, priceEarningsRatioTTM, grahamNumberTTM, enterpriseValueTTM, returnOnInvestedCapitalTTM, \
    enterpriseValueOverEBITDATTM, enterpriseValueOverFreeCashFlowTTM, means_dict

def retrieve_datasTTM(symbol_datas, specific_data, symbol, symbol_dict, bulk_dict, mean_array = None):
    symbol = symbol.replace(".", "-") # some stocks have points in it and that stop from retrieving the datas
    if not symbol_datas or symbol_datas[0][f"{specific_data}"] == None:
        print(f"{specific_data} not found")
    else:
        symbol_dict[symbol] = symbol_datas[0][f"{specific_data}"]
        if specific_data == "price":
            print(f"Price is {symbol_dict[symbol]}")
        if bulk_dict.get(specific_data) == None:
            bulk_dict[specific_data] = []
            bulk_dict[specific_data].append(symbol_datas[0][f"{specific_data}"])
        else:
            bulk_dict[specific_data].append(symbol_datas[0][f"{specific_data}"])
        # after that i should recover datas for every year
        print(f"Found {specific_data}")
        if mean_array != None:
            mean_array.append(symbol_datas[0][f"{specific_data}"])


def retrieve_stock_datas(symbol):
    financial_dict, key_metrics_dict, quote_dict = stock_api_call(symbol)
    return_dict = {}
    symbol = symbol.replace(".", "-") 
    return_dict[symbol] = {}
    counter = 0
    for key in financial_dict:
        date = financial_dict[counter]["date"]
        year = ""
        for i in range(4):
            year += date[i]
        # it will cause a problem if key metrics data go further in the past than financial statements (that souldn't happen normally but ...)
        return_dict[symbol][year] = {}
        return_dict[symbol][year]["financialStatements"] = {}
        return_dict[symbol][year]["financialStatements"] = financial_dict[counter]
        counter+=1
    counter = 0 
    for key in key_metrics_dict:
        date = key_metrics_dict[counter]["date"]
        year = ""
        for i in range(4):
            year += date[i]
        return_dict[symbol][year]["keyMetrics"] = {} 
        return_dict[symbol][year]["keyMetrics"] = key_metrics_dict[counter]
        counter += 1
    return return_dict

def build_stock_dicts(stock_dict, stock: str):
    # maybe add years upper bound and lower bound arguments ?
    # build unique dict for each stock composent like financial statements, key metrics, dcf and then save them to csv ....
    financial_statements_dict = {}
    key_metrics_dict = {}
    for i in range(2022, 2000, -1):
        if stock_dict[stock].get(str(i)) != None:
            if stock_dict[stock][str(i)].get("financialStatements") != None:
                financial_statements_dict[str(i)] = stock_dict[stock][str(i)]["financialStatements"]
            else:
                break
    for i in range(2022, 2000, -1):
        if stock_dict[stock].get(str(i)) != None and stock_dict[stock][str(i)].get("keyMetrics") != None:
            key_metrics_dict[str(i)] = stock_dict[stock][str(i)]["keyMetrics"]
        else:
            break
    dic_to_CSV(financial_statements_dict, f"{stock}_financial_statements")
    dic_to_CSV(key_metrics_dict, f"{stock}_key_metrics")



def catch_data(string):
    clean_string = string.lower().strip().replace(".", "").replace("-", "").replace(" ", "")
    if clean_string[len(clean_string)-1] == "m" and clean_string[len(clean_string)-2] == "t" and clean_string[len(clean_string)-3] == "t":
        clean_string = clean_string[0:len(clean_string)-3]
    if clean_string == "roe" or clean_string == "returnonequity":
        return "roe"
    elif clean_string == "per" or clean_string == "priceearningsratio":
        return "per"
    elif clean_string == "price":
        return "price"
    else:
        return clean_string

#####################################################################################################################################################

                                                        # "MATHS" FUNCTION #

#####################################################################################################################################################


#clean data for mean calculation, type of data is like: roe, per, ev etc
def data_cleaning(array, data: str):
    # need to improve this in the future since it removes too much value on the upper bound i think
    # IF YOU REALLY WANT A CORRECT CLEANING YOU MUST DO IT MANUALLY THIS FUNCTION IS JUST HERE TO FASTEN THE PROCESS AND AVOID CRAZY VALUES (even when
    # they make sense)
    data = data.lower()
    print(data)
    median = np.median(array)
    q1 = np.quantile(array, 0.25)
    q3 = np.quantile(array, 0.75)
    iqr = q3 - q1
    if data == "roe":
        # the widely accepted constant for this type of outliers is 1.5 but in the case of roe it's too small
        upper_bound_outlier = q3 + 2.25*(iqr)
        lower_bound_outlier = q1 - 2.25*(iqr)
    elif data == "per":
        lower_bound_outlier = q1 - 1.5*(iqr)
        upper_bound_outlier = q3 + 1.5*(iqr)
    elif data == "price":
        # only clean the prices for plotting
        lower_bound_outlier = q1 - 1.5*(iqr)
        upper_bound_outlier = q3 + 1.5*(iqr)
    else:
        print(f"Can't clean this type of datas")
        return
    while(True):
            if array[0] > lower_bound_outlier and array[len(array)-1] < upper_bound_outlier:
                # stop if all values are in the range
                break
            elif array[0] < lower_bound_outlier:
                # if the value is out of bound remove it and remove one from the other side too to balance it
                array.pop(0)
                array.pop()
            elif array[len(array)-1] > upper_bound_outlier:
                # same for upper bound
                array.pop()
                array.pop(0)
    print(median, q1, q3, upper_bound_outlier, lower_bound_outlier)
    return array

def market_data_cleaning(dict):
    # clean the entire market datas
    for key in dict:
        data = catch_data(key)
        median = np.median(dict[key])
        q1 = np.quantile(dict[key], 0.25)
        q3 = np.quantile(dict[key], 0.75)
        iqr = q3 - q1 
        if data == "roe":
            # the widely accepted constant for this type of outliers is 1.5 but in the case of roe it's too small
            upper_bound_outlier = q3 + 2.25*(iqr)
            lower_bound_outlier = q1 - 2.25*(iqr)
        elif data == "per":
            lower_bound_outlier = q1 - 1.5*(iqr)
            upper_bound_outlier = q3 + 1.5*(iqr)
        elif data == "price":
            # only clean the prices for plotting
            lower_bound_outlier = q1 - 1.5*(iqr)
            upper_bound_outlier = q3 + 1.5*(iqr)
        while True:
            if dict[key][0] > lower_bound_outlier and dict[key][len(dict[key])-1] < upper_bound_outlier:
                break
            # i don't need two elif i could do just one with an or but idk ...
            elif dict[key][0] < lower_bound_outlier:
                dict[key].pop(0)
                dict[key].pop()
            elif dict[key][len(dict[key])-1] > upper_bound_outlier:
                dict[key].pop()
                dict[key].pop(0)
        return dict



def calculate_means(dict_datas_of_symbols):
    # the argument passed is a dict with the corresponding key and data for example dict["roeMean"] contain an array with all the roe retrieved
    # so we can apply the mean operations
    # maybe check the type of the datas e.g dict or array to adapt
    # return a new variable
    means_dict = {}
    for key in dict_datas_of_symbols:
        if dict_datas_of_symbols[key]: 
            means_dict[key] = statistics.mean(dict_datas_of_symbols[key])
    return means_dict

def calculate_standard_deviation_population(dict_datas):
    # pass the bulk datas dict
    standard_deviation_dict = {}
    for key in dict_datas:
        standard_deviation_dict[key] = statistics.stdev(dict_datas[key])
    return standard_deviation_dict



def scatter_plot(dataframe, x_data, y_data, x_limits: list = None, y_limits: list = None, name_of_the_file="undefined_plot", format="png"):
    if not dataframe.empty and x_data in dataframe.columns and y_data in dataframe.columns:
        cwd = os.getcwd()
        curr_path = f"{cwd}/PLOTS"
        curr_plot =  sns.scatterplot(data=dataframe, x=dataframe[x_data], y=dataframe[y_data])
        if x_limits != None:
            plt.xlim(left=x_limits[0])
            plt.xlim(right=x_limits[1])
        if y_limits != None:
            plt.ylim(bottom=y_limits[0])
            plt.ylim(top=y_limits[1])
            print(plt.ylim())
        plt.savefig(f"{curr_path}/{name_of_the_file}.{format}")
        # clear the current figure otherwise it'll overlap
        plt.clf()
    else:
        if dataframe.empty:
            print(f"The dataframe is empty, can't plot")
        elif x_data not in dataframe.columns:
            print(f"x_data is not a column of the dataframe")
        elif y_data not in dataframe.columns:
            print(f"y_data is not a column of the dataframe")

def histogram_plot(dataframe, x_data, bin_width, x_limits: list = None, name_of_the_file="histogram_plot", format="png", KDE=False):
    if not dataframe.empty and x_data in dataframe.columns:
        cwd = os.getcwd()
        curr_path = f"{cwd}/PLOTS"
        curr_plot = sns.histplot(data=dataframe, x=dataframe[x_data], binwidth=bin_width, kde=KDE)
        if x_limits != None:
            plt.xlim(left=x_limits[0])
            plt.xlim(right=x_limits[1])
        plt.savefig(f"{curr_path}/{name_of_the_file}.{format}")
        # clear the current figure otherwise it'll overlap
        plt.clf()
    else:
        if dataframe.empty:
            print(f"The dataframe is empty")
        elif x_data not in dataframe.columns:
            print(f"x_data is not a column of the dataframe")


#####################################################################################################################################################

                                                            # Pandas and dict manipulation #

#####################################################################################################################################################

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
    # orient=index means the keys of the dictionary will be rows, because before this line the dict keys are columns
    df = pd.DataFrame.from_dict(dic, orient="index")
    df.to_csv(f"{path}/{name}.csv", index=True, header=True)
    return



# populate the classes market and stock
# retrieve the datas for every year
# main function should be available for every markets with data available
# clean datas differently for plotting
# once the general analysis is done make a function that give detailed information about specifics tickers
# check the dates of the datas
# check the price of the datas to see if the datas are not outdated
# normalize the datas for a weighted average and then a score