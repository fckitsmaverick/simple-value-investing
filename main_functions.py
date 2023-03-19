import datetime as dt
import pandas as pd
import os, sys
from dotenv import load_dotenv
import time
import certifi
import json
import math, statistics, numpy as np, seaborn as sns, matplotlib.pyplot as plt

from scipy import stats


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


def api_call(symbol):
    global timer_function_start
    timer_function_start = time.perf_counter()
    count = 0
    for attemps in range(4):
        # check for errors
        try:
            # add enterprise value / ebitda and enterprise value / free cash flow both are in keyMetricsTTM
            financialRatiosTTM = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/ratios-ttm/{symbol}?apikey={apikey}")
            keyMetricsTTM = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{symbol}?apikey={apikey}")
            stockQuoteTTM = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/quote/{symbol}?apikey={apikey}")
            print(f"FOUND TICKER: {symbol}")
            break
        except:
            count += 1
            if count == 5:
                print("Can't find this ticker, will pass")
                break
            print(f"{count} attempts, can't find this ticker, trying again")
            continue
    return stockQuoteTTM, financialRatiosTTM, keyMetricsTTM


def stock_api_call(symbol):
    count = 0
    for attempts in range(4):
        try:
            balanceSheetStatement = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{symbol}?limit=120&apikey={apikey}")
            keyMetrics = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/key-metrics/{symbol}?limit=40&apikey={apikey}")
            cashFlowStatements = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{symbol}?limit=120&apikey={apikey}")
            discountedCashFlow = get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/discounted-cash-flow/{symbol}?apikey={apikey}")
            break
        except:
            count += 1
            if count == 5:
                print("Can't find this ticker")
                break
            print(f"{count} attempts, can't find this ticker, trying again")
    return balanceSheetStatement, keyMetrics, cashFlowStatements, discountedCashFlow


####################################################################################################################################################

                                                        # MAIN FUNCTION #

####################################################################################################################################################

def get_datasTTM(list_of_symbols, limit = 1000000):
    # will problably have to change this function it's doing too much
    #declare the dictionnaries which will store the different data
    print(limit)
    (price, 
     bulk_datas,
       dividendPerShareTTM,
         returnOnEquityTTM,
           priceEarningsRatioTTM,
             grahamNumberTTM,
                grahamNetNetTTM,
               enterpriseValueTTM,
                returnOnInvestedCapitalTTM,
                  enterpriseValueOverEBITDATTM,
                    enterpriseValueOverFreeCashFlowTTM)= ({} for i in range(11))
    
    meanReturnOnEquityTTM, meanPriceEarningsRatioTTM, meanReturnOnInvestedCapitalTTM = ([] for i in range(3))
    counter = 0
    for symbol in list_of_symbols:
        # make the api calls
        stockQuote, financialRatios, keyMetrics = api_call(symbol)
        # retrieve the different datas we are interested in
        retrieve_datasTTM(stockQuote, "price", symbol, price, bulk_datas)
        retrieve_datasTTM(financialRatios, "dividendPerShareTTM", symbol, dividendPerShareTTM, bulk_datas)
        retrieve_datasTTM(financialRatios, "returnOnEquityTTM", symbol, returnOnEquityTTM, bulk_datas, meanReturnOnEquityTTM)
        retrieve_datasTTM(financialRatios, "priceEarningsRatioTTM", symbol, priceEarningsRatioTTM, bulk_datas, meanPriceEarningsRatioTTM)
        retrieve_datasTTM(financialRatios, "returnOnCapitalEmployedTTM", symbol, returnOnInvestedCapitalTTM, bulk_datas, meanReturnOnInvestedCapitalTTM)
        retrieve_datasTTM(keyMetrics, "grahamNumberTTM", symbol, grahamNumberTTM, bulk_datas)
        retrieve_datasTTM(keyMetrics, "grahamNetNetTTM", symbol, grahamNetNetTTM, bulk_datas)
        retrieve_datasTTM(keyMetrics, "enterpriseValueTTM", symbol, enterpriseValueTTM, bulk_datas)
        retrieve_datasTTM(keyMetrics, "enterpriseValueOverEBITDATTM", symbol, enterpriseValueOverEBITDATTM, bulk_datas)
        retrieve_datasTTM(keyMetrics, "evToFreeCashFlowTTM", symbol, enterpriseValueOverFreeCashFlowTTM, bulk_datas)
        counter += 1
        print(f"{counter} ticker(s) retrieved")
        if counter == limit:
            break
        timer_function_end = time.perf_counter()
        print(f"Time elapsed to retrive this ticker : {timer_function_end - timer_function_start}")
        means_dict = {"roeMean" : meanReturnOnEquityTTM, "perMean" : meanPriceEarningsRatioTTM, "roicMean" : meanReturnOnInvestedCapitalTTM}
    return (price, 
            bulk_datas,
              dividendPerShareTTM,
                returnOnEquityTTM,
                  priceEarningsRatioTTM,
                    grahamNumberTTM,
                     grahamNetNetTTM,
                      enterpriseValueTTM,
                      returnOnInvestedCapitalTTM,
                        enterpriseValueOverEBITDATTM,
                         enterpriseValueOverFreeCashFlowTTM,
                           means_dict)


#####################################################################################################################################################



#####################################################################################################################################################



def retrieve_datasTTM(symbol_datas, specific_data, symbol, symbol_dict, bulk_dict, mean_array = None):
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
    time_start = time.perf_counter()
    balance_sheet_dict, key_metrics_dict, cash_flow_dict, discounted_cash_flow_dict = stock_api_call(symbol)
    # check if the ticker is correct
    if not balance_sheet_dict and not key_metrics_dict and not cash_flow_dict and not discounted_cash_flow_dict:
        print("No datas available for this ticker")
        return False
    return_dict = {}
    return_dict[symbol] = {}
    counter = 0
    for key in balance_sheet_dict:
        date = balance_sheet_dict[counter]["date"]
        year = ""
        for i in range(4):
            year += date[i]
        # it will cause a problem if key metrics data go further in the past than financial statements (that souldn't happen normally but ...)
        return_dict[symbol][year] = {}
        return_dict[symbol][year]["balanceSheetStatements"] = {}
        return_dict[symbol][year]["balanceSheetStatements"] = balance_sheet_dict[counter]
        counter+=1
    counter = 0 
    for key in key_metrics_dict:
        date = key_metrics_dict[counter]["date"]
        year = ""
        for i in range(4):
            year += date[i]
        # won't be useful 99% of the time but sometimes the api can give key metrics without balance sheet ?????
        if return_dict[symbol].get(year) == None:
            return_dict[symbol][year] = {}
        return_dict[symbol][year]["keyMetrics"] = {} 
        return_dict[symbol][year]["keyMetrics"] = key_metrics_dict[counter]
        counter += 1
    counter = 0
    for key in cash_flow_dict:
        year = cash_flow_dict[counter]["calendarYear"]
        if return_dict[symbol].get(year) == None:
            return_dict[symbol][year] = {}
        return_dict[symbol][year]["cashFlowStatements"] = {}
        return_dict[symbol][year]["cashFlowStatements"] = cash_flow_dict[counter]
        counter+= 1
    return_dict["currentDCF"] = discounted_cash_flow_dict[0]["dcf"]
    time_end = time.perf_counter()
    print(f"Retrieved datas for stock : {symbol} \nTime needed : {time_end-time_start}")
    return return_dict


def build_stock_dicts(stock_dict, stock: str, market_name):
    # maybe add years upper bound and lower bound arguments ?
    # build unique dict for each stock composent like financial statements, key metrics, dcf and then save them to csv ....
    balance_sheet_dict = {}
    key_metrics_dict = {}
    cash_flow_dict = {}
    discounted_cash_flow_dict = {}
    for year in range(2022, 2000, -1):
        if stock_dict[stock].get(str(year)) != None:
            if stock_dict[stock][str(year)].get("balanceSheetStatements") != None:
                balance_sheet_dict[str(year)] = stock_dict[stock][str(year)]["balanceSheetStatements"]
            else:
                break
    for year in range(2022, 2000, -1):
        if stock_dict[stock].get(str(year)) != None and stock_dict[stock][str(year)].get("keyMetrics") != None:
            key_metrics_dict[str(year)] = stock_dict[stock][str(year)]["keyMetrics"]
        else:
            break
    for year in range(2022, 2000, -1):
        if stock_dict[stock].get(str(year)) != None and stock_dict[stock][str(year)].get("cashFlowStatements") != None:
            cash_flow_dict[str(year)] = stock_dict[stock][str(year)]["cashFlowStatements"]
        else:
            break
    discounted_cash_flow_dict["currentDCF"] = stock_dict["currentDCF"]
    dic_to_CSV(discounted_cash_flow_dict, f"{stock}discountedCashFlow", directory=f"{market_name}/{stock}", transpose=False)
    dic_to_CSV(balance_sheet_dict, f"{stock}balanceSheetStatements", directory=f"{market_name}/{stock}", transpose=False)
    dic_to_CSV(key_metrics_dict, f"{stock}keyMetrics", directory=f"{market_name}/{stock}", transpose=False)
    dic_to_CSV(cash_flow_dict, f"{stock}cashFlowStatements", directory=f"{market_name}/{stock}", transpose=False)



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
        else:
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

def histogram_plot(dataframe, x_data, bin_width, x_limits: list = None, name_of_the_file="histogram_plot", format="png", KDE=True):
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

def dic_to_CSV(dic, name: str, directory: str = None, transpose=False):
    current_directory = os.getcwd()
    path = f"{current_directory}/CSV"
    # orient=index means the keys of the dictionary will be rows, because before this line the dict keys are columns
    df = pd.DataFrame.from_dict(dic, orient="index")
    if transpose == True:
        df = df.transpose()
    if directory != None:
        if not os.path.exists(f"{path}/{directory}"):
            os.mkdir(f"{path}/{directory}")
        df.to_csv(f"{path}/{directory}/{name}.csv")
        return
    df.to_csv(f"{path}/{name}.csv", index=True, header=True)
    return


def estimated_time(size: int):
    estimated_time = (size*3.5)/60
    hours = math.floor(estimated_time/60)
    minutes = math.floor(estimated_time%60)
    print(f"Estimated time to retrieve datas : {hours} hours {minutes} minutes") 
    time.sleep(4.0)

# populate the classes market and stock
# retrieve the datas for every year
# main function should be available for every markets with data available
# clean datas differently for plotting
# once the general analysis is done make a function that give detailed information about specifics tickers
# check the dates of the datas
# check the price of the datas to see if the datas are not outdated
# normalize the datas for a weighted average and then a score