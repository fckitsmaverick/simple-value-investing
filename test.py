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

time_start = time.perf_counter()

sns.set_theme()

load_dotenv()
apikey = os.environ.get("api_key")
 
SP500List = mf.get_SP500_list()

price, main_datas, roe, per, grahamNumber, enterpriseValueTTM, returnOnInvestedCapitalTTM, enterpriseValueOverEBITDATTM, enterpriseValueOverFreeCashFlowTTM, \
    datas_means_dict = mf.get_datasTTM(SP500List)

mf.dic_to_CSV(main_datas, "buldDatas")

clean_datas_dict = {}

# have to clean ROE alone i think
cleaned_price = mf.data_cleaning(main_datas["price"], "price")
cleaned_roe = mf.data_cleaning(datas_means_dict["roeMean"], "roe")
cleaned_per = mf.data_cleaning(datas_means_dict["perMean"], "per")
datas_means_dict["roeMean"] = cleaned_roe
datas_means_dict["perMean"] = cleaned_per
# calculate means function takes a dict so i have to reassignate

final_means_dict = mf.calculate_means(datas_means_dict)
standard_deviation = mf.calculate_standard_deviation_population(main_datas)
print(standard_deviation)



ROETTM_sorted = mf.sorting_dict_values_reversed(roe)
PERTTM_sorted = mf.sorting_dict_values(per)
GrahamNumberTTM_sorted = mf.sorting_dict_values(grahamNumber)
enterpriseValueTTM_sorted = mf.sorting_dict_values(enterpriseValueTTM)


# convert my dictionnary into a CSV File
mf.dic_to_CSV(ROETTM_sorted, "ROE")
mf.dic_to_CSV(enterpriseValueTTM_sorted, "EnterpriseValueTTM")

worth_interest, all_values = ({} for i in range(2))

for symbol in ROETTM_sorted:
    if GrahamNumberTTM_sorted[symbol] >= price[symbol]:
        worth_interest[symbol] = {}
        worth_interest[symbol]["Price"] = price[symbol]
        worth_interest[symbol]["GrahamNumberTTM"] = GrahamNumberTTM_sorted[symbol]
        worth_interest[symbol]["ReturnOnEquityTTM"] = ROETTM_sorted[symbol]
        worth_interest[symbol]["PriceEarningsRatioTTM"] = PERTTM_sorted[symbol]
        worth_interest[symbol]["EnterpriseValueTTM"] = enterpriseValueTTM_sorted[symbol]
        worth_interest[symbol]["EnterpriseValueOverEBITDATTM"] = enterpriseValueOverEBITDATTM[symbol]

for symbol in ROETTM_sorted:
    all_values[symbol] = {}
    all_values[symbol]["Price"] = price[symbol]
    all_values[symbol]["GrahamNumberTTM"] = GrahamNumberTTM_sorted[symbol]
    all_values[symbol]["ReturnOnEquityTTM"] = ROETTM_sorted[symbol]
    all_values[symbol]["PriceEarningsRatioTTM"] = PERTTM_sorted[symbol]
    all_values[symbol]["EnterpriseValueTTM"] = enterpriseValueTTM_sorted[symbol]
    all_values[symbol]["EnterpriseValueOverEBITDATTM"] = enterpriseValueOverEBITDATTM[symbol]

df_market_means = pd.DataFrame.from_dict(final_means_dict, orient="index")

df_worth_interest = pd.DataFrame.from_dict(worth_interest, orient="index")
df_final_worth_interest = pd.concat([df_worth_interest, df_market_means], axis=1)

df_all_values = pd.DataFrame.from_dict(all_values, orient="index")
df_final_all_values = pd.concat([df_all_values, df_market_means], axis=1)

# function for plotting will NOT transpose the dict, meaning that when you turn your dict to a pandas dataframe you MUST include --> orient="index" 
mf.scatter_plot(df_final_all_values, x_data="Price", y_data="ReturnOnEquityTTM", x_limits=[0, 340], y_limits=[-0.50, 0.9], name_of_the_file="roe_scatter_plot")
mf.histogram_plot(df_final_all_values, bin_width=20, x_data="Price", x_limits=[0, 1000])
mf.scatter_plot(df_final_all_values, x_data="Price", y_data="EnterpriseValueTTM", name_of_the_file="price_to_ev_plot")

# transpose put the symbol as index
dict_worth_interest = df_worth_interest.transpose().to_dict()
dict_all_values = df_final_all_values.transpose().to_dict()

mf.dic_to_CSV(dict_worth_interest, "WorthInterest")
mf.dic_to_CSV(dict_all_values, "NotRetainedValue")

SP500 = cls.market("SP500", 2022)
print(SP500.name)

time_end = time.perf_counter()

stock = input("Enter which stock interests you : ")

stock_interest = mf.retrieve_stock_datas(stock)
mf.build_stock_dicts(stock_interest, stock)


print(f"Timer in seconds : {time_end - time_start}")
# roe = net income / total shareholders equity
# enterprise value = market cap + total debt - cash and cash equivalent --> if you wanna buy a company you must repay the company's debt
# so it's much more expensive to buy a company with a lot of debt but when you buy you keep the cash available in the company
# enterprise value / ebitda : the lower the better (if high it's probably overvalued), it's good to compare it with price/earnings ratio, if too high
# the probably may have a lot of debt compared to it's earnings