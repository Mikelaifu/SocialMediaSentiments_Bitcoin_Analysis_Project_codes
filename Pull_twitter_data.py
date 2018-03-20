# Dependencies
import tweepy
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
import time
style.use('ggplot')

from pprint import pprint

# Import and Initialize Sentiment Analyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

from config2 import (Consumer_key, 
                    Consumer_secret, 
                    Access_token, 
                    Access_token_secret)


# Setup Tweepy API1 Authentication (first account)
auth = tweepy.OAuthHandler(Consumer_key, Consumer_secret)
auth.set_access_token(Access_token, Access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())



# define a function to pull data from twitter account and generate CSV file
def pull_tweets_to_csv(target_user, pages):
    
    # part1: get as many tweets as we can
    tweets_list = []
    for x in range(pages):
        response = api.user_timeline(target_user, page=x)
        for tweet in response:
            tweets_list.append(tweet)
    print(f"We have {len(tweets_list)} tweets from account: {target_user}.")
    start = datetime.strptime(tweets_list[0]['created_at'], "%a %b %d %H:%M:%S %z %Y")
    end = datetime.strptime(tweets_list[len(tweets_list)-1]['created_at'], "%a %b %d %H:%M:%S %z %Y")
    recent_date = f"{start.year}{start.month}{start.day}"
    oldest_date = f"{end.year}{end.month}{end.day}"
    print(f"Those tweets from {oldest_date} to {recent_date}.")
    
    # part2: extract data from pulled tweets and generate lists for next
    Acc_name = []
    Tweet_date = []
    Tweet_id = []
    Text = []
    Favor_count = []
    Retweet_count = []
    Lan = []
    Acc_date = []
    followers_count = []
    Acc_location = []
    
    for tweet in tweets_list:
        Acc_name.append(tweet['user']['screen_name'])
        Tweet_date.append(tweet['created_at'])
        Tweet_id.append(tweet['id_str'])
        Text.append(tweet['text'])
        Favor_count.append(tweet['favorite_count'])
        Retweet_count.append(tweet['retweet_count'])
        Lan.append(tweet['lang'])
        Acc_date.append(tweet['user']['created_at'])
        followers_count.append(tweet['user']['followers_count'])
        Acc_location.append(tweet['user']['location'])
    
    # part3: generate data frame
    df = pd.DataFrame({
        "Account Name": Acc_name,
        "Tweet Date": Tweet_date,
        "Tweet ID": Tweet_id,
        "Text": Text,
        "Favorite Count": Favor_count,
        "Retweet Count": Retweet_count,
        "Language": Lan,
        "Account Created Date": Acc_date,
        "Followers Count": followers_count,
        "Account Location": Acc_location
    })
    df=df[["Account Name", "Tweet Date", "Tweet ID", "Text", "Favorite Count", "Retweet Count", "Language", 
       "Account Created Date", "Followers Count", "Account Location"]]
    
    # part4: sentiment analysis and add results to data frame
    df["Compound"] = ""
    df["Positive"] = ""
    df["Negative"] = ""
    df["Neutral"] = ""
    for index, row in df.iterrows():
        results = analyzer.polarity_scores(row["Text"])
        df.set_value(index, 'Compound', results['compound'])
        df.set_value(index, 'Positive', results['pos'])
        df.set_value(index, 'Negative', results['neg'])
        df.set_value(index, 'Neutral', results['neu'])
    
    # part5: save data to CSV file
    filename = f"{oldest_date}-{recent_date}-{target_user}.csv"
    df.to_csv(filename)


    #"@Coinsquare", '@Coinbase', "@krakenfx", "@cex_io",  "@Gemini", "@binance_2017",

#target_user = []

for target in target_user:
    
    pull_tweets_to_csv(target, 100)