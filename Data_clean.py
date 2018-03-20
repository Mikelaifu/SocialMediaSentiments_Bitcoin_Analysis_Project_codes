import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import datetimes
import time

def clean_Group_data(filename):
    x = pd.read_csv(filename)
    mask = x['Tweet Date'].apply(lambda x: len(x) == 30)
    mask1 = x['Language'] == 'en'
    mask2 = x['Compound'].notnull()
    df = x[mask&mask1&mask2]
    timelist = []
    for tweet_date in df['Tweet Date']: 
        tweet_datetime = pd.to_datetime(tweet_date)
        tweet_datetime = str(tweet_datetime)
        unix = time.mktime(datetime.datetime.strptime(tweet_datetime, "%Y-%m-%d %H:%M:%S").timetuple())
        timelist.append(time.strftime('%Y-%m-%d', time.localtime(unix)))
    df['Format_date'] = timelist
    cleaned_data = df.groupby('Format_date').agg({"Text": "count", "Compound" : "mean"})
    return cleaned_data


file_list = glob.glob("*.csv")
cleanedDataDict = {}
for Datafile in file_list:
    dataFrame = clean_Group_data(Datafile)
    cleanedDataDict[Datafile] = dataFrame
