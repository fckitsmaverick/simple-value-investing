import statistics

import main_functions as mf

class market:
    pass
    def __init__(self, name, year):
        self.name = name
        self.year = year
    
    def market_availability(self, name, year):
        pass
    
    def market_data_cleaning(self, dict):
        # return a dict
        cleaned_datas = mf.market_data_cleaning(dict)
        return cleaned_datas

    def market_means(self, dict):
        means_dict = mf.calculate_means(dict)
        return means_dict 
    
    def market_standard_deviations(self, dict):
        stddv_dict = mf.calculate_standard_deviation_population(dict)
        return stddv_dict
    

class stock:
    pass
