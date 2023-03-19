import main_functions as mf
import os
import sys

import datas_retrieving
import MarkowitzModel

from market import market_analysis

apikey = os.environ.get("api_key")

def user_market():
    ans = input("Which market do you want to analyze ? ")
    clean_ans = ans.lower().replace(" ", "")
    if clean_ans == "nyse" or clean_ans == "nasdaq" or clean_ans == "euronext" or clean_ans == "amex" or clean_ans == "tsx":
        market = datas_retrieving.get_exchange(clean_ans)
    elif clean_ans == "sp500":
        market = datas_retrieving.get_SP500()
    elif clean_ans == "cac40":
        market = datas_retrieving.get_CAC40()
    elif clean_ans == "paris" or clean_ans=="oss117":
        market = datas_retrieving.faut_absolument_que_jappelle_Armand()
    elif clean_ans == "london" or clean_ans == "lse":
        market = datas_retrieving.get_LSE()
    elif clean_ans == "shenzhen" or clean_ans == "szse":
        market = datas_retrieving.get_SHENZHEN()
    elif clean_ans == "hkse" or clean_ans == "hong kong":
        market = datas_retrieving.get_HKSE()
    elif clean_ans == "tokyo" or clean_ans == "tse" or clean_ans == "tyo":
        market = datas_retrieving.get_TKSE()
    elif clean_ans == "shanghai" or clean_ans == "sse" or clean_ans == "shh":
        market = datas_retrieving.get_SSE() 
    elif clean_ans == "bangkok" or clean_ans == "set" or clean_ans == "thailand":
        market = datas_retrieving.get_SET()
    elif clean_ans == "moscow" or clean_ans == "mcx":
        market = datas_retrieving.get_MCX()
    elif clean_ans == "madrid" or clean_ans == "spain" or clean_ans == "mc" or clean_ans == "bme":
        market = datas_retrieving.get_BME()
    elif clean_ans == "singapore" or clean_ans == "sgx":
        market = datas_retrieving.get_SGX()
    elif clean_ans == "jakarta" or clean_ans == "jsx" or clean_ans == "indonesia":
        market = datas_retrieving.get_JSX()
    elif clean_ans == "market" or clean_ans == "markets":
        print("Markets and Indexes currently available are:\nSP500, NYSE, NASDAQ, EURONEXT, AMEX, TORONTO(TSX), CAC40, PARIS, LONDON(LSE), SHENZEN(SZSE),\nHONG-KONG(HKSE), TOKYO(TSE), SHANGHAI(SHH), BANGKOK(SET), MOSCOW(MCX),\nßMADRID(BME), SINGAPORE(SGX), JAKARTA(JSX)")
        user_market()
    else:
        print("Market not supported add the moment. Type MARKETS to see the markets available")
        user_market()
    return market, clean_ans 


def user_tickers():
    user_inp = input("Please enter the stock(s) symbol(s) that you want to analyze (use a comma to separate the tickers): ")
    symbols = user_inp.split(",")
    for i in range(0, len(symbols)):
        new_s = symbols[i].strip().replace(" ", "").upper()
        symbols[i] = str(new_s)
    return symbols


def stock_screener_input(user_request=False):
    # This function is UGLY
    if user_request == False:
        answer = input("""Do you want to run a stock screener? Y/N: """)
    if user_request == False and answer == "N":
        return False
    elif user_request == True or (answer and answer == "Y"):
        print("Now enter your parameters, if you want to pass a parameter press ENTER")
        try:
            marketCapMoreThan = int(input("Enter lower Bound for Market Cap: "))
        except(ValueError):
            marketCapMoreThan = 0
        try:
            marketCapLowerThan = int(input("Enter upper Bound for Market Cap: ") or 90000000)
        except(ValueError):
            marketCapLowerThan = 9000000000000
        try:
            priceMoreThan = int(input("Enter lower bound for Price: "))
        except(ValueError):
            priceMoreThan = 0
        try:
            priceLowerThan = int(input("Enter upper bound for Price: "))
        except(ValueError):
            priceLowerThan = 9000000000000
        try:
            betaMoreThan = int(input("Enter lower bound for Beta: "))
        except(ValueError):
            betaMoreThan = -100000
        try:
            betaLowerThan = int(input("Enter upper bound for Beta: "))
        except(ValueError):
            betaLowerThan = 100000
        try:
            volumeMoreThan = int(input("Enter lower bound for Volume: "))
        except(ValueError):
            volumeMoreThan = 0
        try:
            volumeLowerThan = int(input("Enter upper bound for Volume: "))
        except(ValueError):
            volumeLowerThan = 9000000000000
        try:
            dividendMoreThan = int(input("Enter lower bound for Dividend: "))  
        except(ValueError):
            dividendMoreThan = 0
        try:
            dividendLowerThan = int(input("Enter upper bound for Dividend: "))
        except(ValueError):
            dividendLowerThan = 9000000000000
        try:
            sector = str(input("Enter sector: "))
        except(ValueError):
            sector = ""
        try:
            industry = str(input("Enter industry: "))
        except(ValueError):
            industry = ""
        try:
            country = str(input("Enter country: "))
        except(ValueError):
            country = "US"
        try:
            exchange = str(input("Enter exchange: "))
        except(ValueError):
            exchange = "NYSE"
        try:
            limit = input("Enter limit: ")
        except(ValueError):
            limit = 9000000000000
        stock_screener(marketCapMoreThan=marketCapMoreThan, marketCapLowerThan=marketCapLowerThan, priceMoreThan=priceMoreThan,
                       priceLowerThan=priceLowerThan, betaMoreThan=betaMoreThan, betaLowerThan=betaLowerThan, volumeMoreThan=volumeMoreThan,
                         volumeLowerThan=volumeLowerThan, dividendMoreThan=dividendMoreThan, dividendLowerThan=dividendLowerThan,
                            isETF=False, isActivelyTrading=True, sector=sector, industry=industry, country=country, exchange=exchange, limit=limit)
        

# this one should go with main functions and api calls
def stock_screener(marketCapMoreThan: int = 0, marketCapLowerThan: int = 9000000000000, priceMoreThan: int = 0, priceLowerThan: int = 9000000000000,
                   betaMoreThan: int = -100000, betaLowerThan: int = 100000, volumeMoreThan: int = 0, volumeLowerThan: int = 9000000000000, 
                   dividendMoreThan: int = 0, dividendLowerThan: int = 9000000000000, isETF: bool = False, isActivelyTrading: bool = True,
                   sector: str = "", industry: str = "", country: str = "US", exchange: str = "NYSE", limit: int = 9000000000000  
                   ):
    print(marketCapLowerThan)
    # make an api call for this stock research
    # break this line really
    dict_of_company = mf.get_jsonparsed_data(f"https://financialmodelingprep.com/api/v3/stock-screener?marketCapMoreThan={marketCapMoreThan}&marketCapLowerThan={marketCapLowerThan}&priceMoreThan={priceMoreThan}&priceLowerThan={priceLowerThan}&betaMoreThan={betaMoreThan}&betaLowerThan={betaLowerThan}&volumeMoreThan={volumeMoreThan}&volumeLowerThan={volumeLowerThan}&dividendMoreThan={dividendMoreThan}&dividendLowerThan={dividendLowerThan}&sector={sector}&industry={industry}&Country={country}&exchange={exchange}&limit={limit}&apikey={apikey}")
    print(dict_of_company)
    return dict_of_company

def markowitz_input():
    tickers = input("Which stocks do you want to include in your portfolio ? ")
    tickers = tickers.split(",")
    # Why am i forced to do that seriously ?
    stocks = []
    for ticker in tickers:
        curr = ticker.upper().replace(" ", "").strip()
        stocks.append(curr)
    return stocks


def user_input():
    user_input = input("If you want to exit the program type q, else type a command or HELP: ")
    clean_input = user_input.lower().replace(" ", "")
    if clean_input == "q":
        sys.exit()
    elif clean_input == "help":
        print("""
        Commands are:

        q: for exiting program
        screener: for stock screening
        stock: for specific stocks analyzes
        market: for market analysis

        These commands are not case sensitive
              """)
        return True
    elif clean_input == "screener":
        stock_screener_input(user_request=True)
    elif clean_input == "stock":
        user_tickers()
    elif clean_input == "market":
        market_analysis()
    elif clean_input == "markowitz":
        MarkowitzModel.modeling()
        

# check that user input is correct ?