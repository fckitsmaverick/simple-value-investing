import os
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import time 
import sys
import numpy as np, seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats

import main_functions as mf
import classes as cls
import main_input as inp
import datas_retrieving


def market_analysis(market_name):

    time_start = time.perf_counter()

    load_dotenv()
    apikey = os.environ.get("api_key")
    
    market_dict = {
    "nyse": datas_retrieving.get_exchange,
    "nasdaq": datas_retrieving.get_exchange,
    "euronext": datas_retrieving.get_exchange,
    "amex": datas_retrieving.get_exchange,
    "tsx": datas_retrieving.get_exchange,
    "sp500": datas_retrieving.get_SP500,
    "cac40": datas_retrieving.get_CAC40,
    "paris": datas_retrieving.faut_absolument_que_jappelle_Armand,
    "oss117": datas_retrieving.faut_absolument_que_jappelle_Armand,
    "london": datas_retrieving.get_LSE,
    "lse": datas_retrieving.get_LSE,
    "shenzen": datas_retrieving.get_SHENZHEN,
    "szse": datas_retrieving.get_SHENZHEN,
    "hkse": datas_retrieving.get_HKSE,
    "hong kong": datas_retrieving.get_HKSE,
    "tokyo": datas_retrieving.get_TKSE,
    "tse": datas_retrieving.get_TKSE,
    "tkse": datas_retrieving.get_TKSE,
    "shanghai": datas_retrieving.get_SSE,
    "sse": datas_retrieving.get_SSE,
    "bangkok": datas_retrieving.get_SET,
    "set": datas_retrieving.get_SET,
    "moscow": datas_retrieving.get_MCX,
    "mcx": datas_retrieving.get_MCX,
    "madrid": datas_retrieving.get_BME,
    "bme": datas_retrieving.get_BME,
    "singapore": datas_retrieving.get_SGX,
    "sgx": datas_retrieving.get_SGX,
    "jakarta": datas_retrieving.get_JSX,
    "jsx": datas_retrieving.get_JSX,
}

    limit = 5
    try:
        tickers = market_dict[market_name](market_name) 
    except TypeError:
        tickers = market_dict[market_name]()

    bulk_prices, bulk_financial_ratios, bulk_key_metrics = mf.get_datasTTM(tickers, limit)

    # convert bulk datas to dataframe to facilitate calculation later.
    df_prices = pd.DataFrame.from_dict(bulk_prices, orient="index")
    df_financial_ratios = pd.DataFrame.from_dict(bulk_financial_ratios, orient="index")
    df_key_metrics = pd.DataFrame.from_dict(bulk_key_metrics, orient="index")

    # every mean
    #df_prmean = stats.trim_mean(df_prices.loc[:, 'price'], 0.05)
    df_prices_means = df_prices.mean(axis=0).round(3)
    df_mean_key_metrics = df_key_metrics.mean(axis=0).round(3)
    df_mean_financial_ratios = df_financial_ratios.mean(axis=0).round(3)
    df_prices.insert(1, "diffwithmean", df_prices['price']-df_prices_means['price'], True)
    # need to concat
    df_concat_means = pd.concat([df_prices_means, df_mean_key_metrics, df_mean_financial_ratios])

    # center the data for Standard Normal Distribution
    df_centered_key_metrics = df_key_metrics.apply(lambda x: x-x.mean(), axis=0)
    df_centered_financial_ratios = df_financial_ratios.apply(lambda x: x-x.mean(), axis=0)
    # Test Shapiro-Wilk ? Probably Useless.

    # concatenate the 2 dict for ratios so i can pass it to build dict function
    df = pd.concat([df_financial_ratios.T, df_key_metrics.T, df_prices.T], axis=0)
    dict_build = df.to_dict(orient="dict")

    mf.dic_to_CSV(bulk_financial_ratios, "bulkFinancialRatios", f"{market_name}")
    mf.dic_to_CSV(bulk_key_metrics, "bulkKeyMetrics", f"{market_name}")

    mf.df_to_csv(df_concat_means, "meansDatas", market_name)


    # have to clean ROE alone i think
    worth_interest, all_values = ({} for i in range(2))


    params = ["price", "roeTTM", "dividendPerShareTTM", "priceEarningsRatioTTM", "returnOnCapitalEmployedTTM", "grahamNumberTTM", "grahamNetNetTTM",\
               "enterpriseValueTTM", "evToFreeCashFlowTTM", "debtToAssetsTTM", "interestCoverageRatioTTM", "capexToRevenueTTM",\
                "daysPayablesOutstandingTTM", "daysOfInventoryOutstandingTTM", "growthFreeCashFlow"]

    all_values, graham_classification = mf.build_market_dicts(dict_build, params=params)

    mf.dic_to_CSV(all_values, "allValues", f"{market_name}", False)
    mf.dic_to_CSV(graham_classification, "graham_classification", f"{market_name}", False)

    mf.aws_s3_upload(market=market_name)
    
    # should move this in it's own function

    time_end = time.perf_counter()


    print(f"Timer in seconds : {time_end - time_start}")
    # roe = net income / total shareholders equity
    # enterprise value = market cap + total debt - cash and cash equivalent --> if you wanna buy a company you must repay the company's debt
    # so it's much more expensive to buy a company with a lot of debt but when you buy you keep the cash available in the company
    # enterprise value / ebitda : the lower the better (if high it's probably overvalued), it's good to compare it with price/earnings ratio, if too high
    # the probably may have a lot of debt compared to it's earnings