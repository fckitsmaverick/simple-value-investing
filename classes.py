import statistics

import main_functions as mf

class market:
    def __init__(self, name: list, year= None):
        self.name = name
        self.year = year
    


    def market_availability(self, name, year):
        pass
    
    def market_data_cleaning(self, dict):
        # return a dict
        cleaned_datas = mf.market_data_cleaning(dict)
        return cleaned_datas

class stock:
    pass
