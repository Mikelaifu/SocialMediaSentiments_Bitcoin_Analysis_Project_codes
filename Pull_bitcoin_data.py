import os
import numpy as np
import pandas as pd
import pickle
# pickle to serialize and save the downloaded data as a file, which will prevent our script from re-downloading the same data each time we run the script. 
import quandl
from datetime import datetime
import matplotlib.pyplot as plt
from pprint import pprint
import json
import time
import requests

# We'll also import Plotly and enable the offline mode.

#--------------------------------------------------bitcoin & different excahnge------------------------------------------
import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
py.init_notebook_mode(connected = True)

# get bitcoin data
def quandl_bitcoin(exchange):
    
    return quandl.get(f'BCHARTS/{exchange}USD')
# save as the dataset
exchanges = ['KRAKEN','COINBASE','BITSTAMP','ITBIT']
BTC_Dataset= {}
for exchange in exchanges:
    data= quandl_bitcoin(exchange)
    BTC_Dataset[exchange] = data['Weighted Price']
    BTC_Dataset[exchange].replace(0, np.nan, inplace = True)

# save weighted avg price from different exchange 
btc_dataset = pd.DataFrame.from_dict(BTC_Dataset)
btc_dataset["Avg_price"] = btc_dataset.mean(axis = 1)
btc_dataset.fillna(0)
btc_dataset.to_csv("btc_dataset.csv")


# ----------------------------------------bitcoin & crypotocurrency-----------------------------------

#https://poloniex.com/public?command=returnChartData&currencyPair=BTC_ETH&start=1420092000.0&end=1520108705.338483&period=86400
base_url = 'https://poloniex.com/public?command=returnChartData&currencyPair={}&start={}&end={}&period={}'
start_date = datetime.strptime('2015-01-01', '%Y-%m-%d') # get data from the start of 2015
end_date = datetime.now() # up until today
period = 86400

# export into a dataframe
def merge_dfs_on_column(dataframes, labels, col):
   
    series_dict = {}
    for index in range(len(dataframes)):
        series_dict[labels[index]] = dataframes[index][col]
        # return a dictionary with {'COINBASE':'Weighted Price info..', .......}
    return pd.DataFrame(series_dict)

# extract data from different crypoto
def crypotocurrency_data(crypoto, startDate, period ):
    crypoto_dict = {}
    end_date = datetime.now().timestamp()
    start_date = datetime.strptime(startDate, "%Y-%m-%d").timestamp()
    base_url = 'https://poloniex.com/public?command=returnChartData'
    url = f"{base_url}&currencyPair=BTC_{crypoto}&start={start_date}&end={end_date}&period={period}"
    response = requests.get(url).json()
    dataframe =pd.DataFrame.from_dict(response)
    
    dataframe["Date"] = [time.strftime("%Y-%m-%d", time.localtime(int(date))) for date in dataframe["date"]]
    dataframe.set_index('Date', inplace= True)
    #crypoto_dict[crypoto] = dataframe['weightedAverage']
    
    return dataframe
    
currencies = ['ETH','LTC','XRP','DASH']
currency_dict = {}
for currency in currencies:
    
    dataframe = crypotocurrency_data(currency, "2015-01-01", 86400 )
    currency_dict[currency] = dataframe

for currency in currencies:
    currency_dict[currency]['price_usd'] = currency_dict[currency]['weightedAverage'] * btc_dataset["Avg_price"]

combined_df= merge_dfs_on_column(list(currency_dict.values()), list(currency_dict.keys()), 'price_usd' )

combined_df = pd.read_csv("combined_df.csv")