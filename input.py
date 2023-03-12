import main_functions as mf
import os
import sys
apikey = os.environ.get("api_key")


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


def user_input():
    user_input = input("If you want to exit the program type q, else type a command or HELP: ")
    clean_input = user_input.lower().replace(" ", "")
    if clean_input == "q":
        sys.exit()
    elif clean_input == "help":
        print("""
        Commands are:

        q : for exiting program
        screener : for stock screening
        stock : for specific stocks analyzes

        These commands are not case sensitive
              """)
        return True
    elif clean_input == "screener":
        stock_screener_input(user_request=True)
        return True
    elif clean_input == "stock":
        user_tickers()
        return True


# check that user input is correct ?