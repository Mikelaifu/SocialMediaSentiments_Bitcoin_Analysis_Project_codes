import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy


# open btc csv clean and get ready
btc = pd.read_csv('btc_dataset.csv')
btc['Date'] = pd.to_datetime(btc['Date'])#
btc= btc.set_index('Date')
Btc = pd.DataFrame(btc.ix['2015-01-01':, "Avg_price"]).rename(columns = {'Avg_price':'BTC_Price'})
# open comb_df csv clean and get ready
combo_df = pd.read_csv('combined_df.csv')
combo_df = combo_df.rename(columns = {'Unnamed: 0':"Date"})
combo_df['Date'] = pd.to_datetime(combo_df['Date'])
combo_df = combo_df.set_index('Date')
# merge wanted info togather as total bitcoin_crypoto dataset
df_Bitcoin = combo_df.merge(Btc, how = "outer", left_index = True, right_index = True)