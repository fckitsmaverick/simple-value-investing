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
import market_aws

if __name__ == "__main__":
    
    time_start = time.perf_counter()
    markets = ["tse", "nyse"]
    for i in range(0, len(markets)):
        market_aws.market_analysis(markets[i])
    time_end = time.perf_counter()

    print(f"Timer in seconds : {time_end - time_start}")
# roe = net income / total shareholders equity
# enterprise value = market cap + total debt - cash and cash equivalent --> if you wanna buy a company you must repay the company's debt
# so it's much more expensive to buy a company with a lot of debt but when you buy you keep the cash available in the company
# enterprise value / ebitda : the lower the better (if high it's probably overvalued), it's good to compare it with price/earnings ratio, if too high
# the probably may have a lot of debt compared to it's earnings