import os
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import time 
import sys
import numpy as np, seaborn as sns
import matplotlib.pyplot as plt

import main_functions as mf
import classes as cls
import main_input as inp


def market_analysis():

    time_start = time.perf_counter()

    load_dotenv()
    apikey = os.environ.get("api_key")
    
    marketPick, market_name = inp.user_market()

    try:
        limit = int(input("Do you want to set a limit ? (if not press ENTER): "))
    except(ValueError):
        limit = 100000

    bulk_prices, bulk_financial_ratios, bulk_key_metrics = mf.get_datasTTM(marketPick, limit)

    # convert bulk datas to dataframe to facilitate calculation later.
    df_prices = pd.DataFrame.from_dict(bulk_prices, orient="index")
    df_financial_ratios = pd.DataFrame.from_dict(bulk_financial_ratios, orient="index")
    df_key_metrics = pd.DataFrame.from_dict(bulk_key_metrics, orient="index")

    # concatenate the 2 dict for ratios so i can pass it to build dict function
    df = pd.concat([df_financial_ratios.T, df_key_metrics.T, df_prices.T], axis=0)
    dict_build = df.to_dict(orient="dict")
    print(df.to_string())


    mf.dic_to_CSV(bulk_financial_ratios, "bulkFinancialRatios", f"{market_name}")
    mf.dic_to_CSV(bulk_key_metrics, "bulkKeyMetrics", f"{market_name}")


    # have to clean ROE alone i think
    worth_interest, all_values = ({} for i in range(2))


    params = ["price", "roeTTM", "dividendPerShareTTM", "priceEarningsRatioTTM", "returnOnCapitalEmployedTTM", "grahamNumberTTM", "grahamNetNetTTM",\
               "enterpriseValueTTM", "evToFreeCashFlowTTM", "debtToAssetsTTM", "interestCoverageRatioTTM", "capexToRevenueTTM",\
                "daysPayablesOutstandingTTM", "daysOfInventoryOutstandingTTM"]

    user_params = input("Which ratios do you want to include in your CSV files ? (If you want the defaults one press ENTER): ").split(",")
    print(user_params)
    if user_params != [""]:
        params = []
        for param in user_params:
            curr = param.replace(" ", "")
            params.append(curr)

    all_values, graham_classification = mf.build_market_dicts(dict_build, params=params)

    mf.dic_to_CSV(all_values, "allValues", f"{market_name}", False)
    mf.dic_to_CSV(graham_classification, "graham_classification", f"{market_name}", False)

    # function for plotting will NOT transpose the dict, meaning that when you turn your dict to a pandas dataframe you MUST include --> orient="index" 
    # transpose put the symbol as index

    symbols = inp.user_tickers()
    print(symbols)
    if symbols[0] != "":
        for symbol in symbols:
            stock_dict = mf.retrieve_stock_datas(symbol)
            if stock_dict == False:
                continue
            mf.build_stock_dicts(stock_dict, symbol, market_name)

    inp.stock_screener_input()

    answer = inp.user_input()
    if answer == True: inp.user_input()

    time_end = time.perf_counter()


    print(f"Timer in seconds : {time_end - time_start}")
    # roe = net income / total shareholders equity
    # enterprise value = market cap + total debt - cash and cash equivalent --> if you wanna buy a company you must repay the company's debt
    # so it's much more expensive to buy a company with a lot of debt but when you buy you keep the cash available in the company
    # enterprise value / ebitda : the lower the better (if high it's probably overvalued), it's good to compare it with price/earnings ratio, if too high
    # the probably may have a lot of debt compared to it's earnings