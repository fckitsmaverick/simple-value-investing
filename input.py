def user_input():
    user_inp = input("Please enter the stock(s) symbol(s) that you want to analyze (use a comma to separate the tickers): ")
    symbols = user_inp.split(",")
    for i in range(0, len(symbols)):
        new_s = symbols[i].strip().replace(" ", "").upper()
        symbols[i] = str(new_s)
    return symbols


# check that user input is correct ?