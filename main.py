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
import input as inp

time_start = time.perf_counter()

sns.set_theme()

load_dotenv()
apikey = os.environ.get("api_key")
 
marketPick, market_name = inp.user_market()

price, market_datas, dividendPerShareTTM, returnOnEquityTTM, priceEarningsRatioTTM, grahamNumber, grahamNetNetTTM, enterpriseValueTTM, returnOnInvestedCapitalTTM, enterpriseValueOverEBITDATTM, enterpriseValueOverFreeCashFlowTTM, \
datas_means_dict = mf.get_datasTTM(marketPick)

mf.dic_to_CSV(market_datas, "bulkDatas", f"{market_name}")

clean_datas_dict = {}

# have to clean ROE alone i think
cleaned_market_datas = mf.market_data_cleaning(market_datas)

meansTTM = mf.calculate_means(cleaned_market_datas)
standardDeviationTTM = mf.calculate_standard_deviation_population(cleaned_market_datas)
mf.dic_to_CSV(meansTTM, "meansDict", f"{market_name}")
mf.dic_to_CSV(standardDeviationTTM, "standardDeviation", f"{market_name}")

ROETTM_sorted = mf.sorting_dict_values_reversed(returnOnEquityTTM)
GrahamNumberTTM_sorted = mf.sorting_dict_values(grahamNumber)


# convert my dictionnary into a CSV File
mf.dic_to_CSV(ROETTM_sorted, "ROE", f"{market_name}")

worth_interest, all_values = ({} for i in range(2))

for symbol in ROETTM_sorted:
    if GrahamNumberTTM_sorted[symbol] >= price[symbol]:
        worth_interest[symbol] = {}
        worth_interest[symbol]["Price"] = price[symbol]
        worth_interest[symbol]["dividendPerShare"] = dividendPerShareTTM[symbol]
        worth_interest[symbol]["GrahamNumberTTM"] = GrahamNumberTTM_sorted[symbol]
        worth_interest[symbol]["grahamNetNetTTM"] = grahamNetNetTTM[symbol]
        worth_interest[symbol]["ReturnOnEquityTTM"] = ROETTM_sorted[symbol]
        worth_interest[symbol]["PriceEarningsRatioTTM"] = priceEarningsRatioTTM[symbol]
        worth_interest[symbol]["EnterpriseValueTTM"] = enterpriseValueTTM[symbol]
        worth_interest[symbol]["EnterpriseValueOverEBITDATTM"] = enterpriseValueOverEBITDATTM[symbol]

for symbol in ROETTM_sorted:
    all_values[symbol] = {}
    all_values[symbol]["Price"] = price[symbol]
    all_values[symbol]["dividendPerShareTTM"] = dividendPerShareTTM[symbol]
    all_values[symbol]["GrahamNumberTTM"] = GrahamNumberTTM_sorted[symbol]
    all_values[symbol]["grahamNetNetTTM"] = grahamNetNetTTM[symbol]
    all_values[symbol]["ReturnOnEquityTTM"] = ROETTM_sorted[symbol]
    all_values[symbol]["PriceEarningsRatioTTM"] = priceEarningsRatioTTM[symbol]
    all_values[symbol]["EnterpriseValueTTM"] = enterpriseValueTTM[symbol]
    all_values[symbol]["EnterpriseValueOverEBITDATTM"] = enterpriseValueOverEBITDATTM[symbol]

df_market_means = pd.DataFrame.from_dict(meansTTM, orient="index")
df_standard_deviation = pd.DataFrame.from_dict(standardDeviationTTM, orient="index")

df_worth_interest = pd.DataFrame.from_dict(worth_interest, orient="index")
df_final_worth_interest = pd.concat([df_worth_interest, df_market_means], axis=1)

df_all_values = pd.DataFrame.from_dict(all_values, orient="index")
df_final_all_values = pd.concat([df_all_values, df_market_means], axis=1)

# function for plotting will NOT transpose the dict, meaning that when you turn your dict to a pandas dataframe you MUST include --> orient="index" 
mf.scatter_plot(df_final_all_values, x_data="Price", y_data="ReturnOnEquityTTM", x_limits=[0, 340], y_limits=[-0.50, 0.9], name_of_the_file="roe_scatter_plot")
mf.histogram_plot(df_final_all_values, bin_width=20, x_data="Price", x_limits=[0, 500])
mf.scatter_plot(df_final_all_values, x_data="Price", y_data="EnterpriseValueTTM", name_of_the_file="price_to_ev_plot")

# transpose put the symbol as index
dict_worth_interest = df_worth_interest.transpose().to_dict()
dict_all_values = df_final_all_values.transpose().to_dict()

mf.dic_to_CSV(dict_worth_interest, "WorthInterest", f"{market_name}")
mf.dic_to_CSV(dict_all_values, "allValues", f"{market_name}")

SP500 = cls.market("SP500", 2022)

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