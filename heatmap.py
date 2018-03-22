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
import json
from pprint import pprint

# We'll also import Plotly and enable the offline mode.

import plotly.offline as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
py.init_notebook_mode(connected = True)



def correlation_heatmap(df, title, absolute_bounds=True):
    '''Plot a correlation heatmap for the entire dataframe'''
    heatmap = go.Heatmap(
        z=df.corr(method='pearson').as_matrix(),
        x=df.columns,
        y=df.columns,
        colorbar=dict(title='Pearson Coefficient'),
    )
    
    layout = go.Layout(title=title)
    
    if absolute_bounds:
        heatmap['zmax'] = 1.0
        heatmap['zmin'] = -1.0
        
    fig = go.Figure(data=[heatmap], layout=layout)
    py.iplot(fig)

df_2016 = df_sentiment_org[df.index.year == 2016]
df_2016.pct_change().corr(method= 'pearson')

correlation_heatmap(df_2016.pct_change().corr(method= 'pearson'), "Correlation_2016")