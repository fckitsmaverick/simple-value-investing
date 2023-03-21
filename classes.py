import statistics

import main_functions as mf

class market:

    def __init__(self, name: list, year= None):
        self.name = name
        self.year = year
        self.price_mean = None
        self.price_std = None
        self.return_mean = None
        self.return_std = None
    
    def market_availability(self, name, year):
        pass
    
    def market_data_cleaning(self, dict):
        # return a dict
        cleaned_datas = mf.market_data_cleaning(dict)
        return cleaned_datas

class stock:
    pass
