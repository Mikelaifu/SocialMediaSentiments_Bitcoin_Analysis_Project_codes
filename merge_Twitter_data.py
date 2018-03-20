
#merge text_count into one for analysis

df_tweet_count= pd.DataFrame(cleanedDataDict[file_list[0]]["Text"]).merge(pd.DataFrame(cleanedDataDict[file_list[1]]["Text"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[2]]["Text"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[3]]["Text"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[4]]["Text"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[5]]["Text"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[6]]["Text"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[7]]["Text"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[8]]["Text"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[9]]["Text"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[10]]["Text"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[11]]["Text"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[12]]["Text"]), how = "outer", 
                                    left_index = True, right_index = True)


# ********************************************************************************************************************************************************
# create count for each row into a new columns
df_tweet_count = df_tweet_count.fillna(0)
tweet_count = []
for Iindex in list(df_tweet_count.index):
    tweet_count.append(df_tweet_count.ix[Iindex].sum())

df_tweet_count['Tweet_count'] = tweet_count


#-----------------------------------------------------Compound merge------------------------------------------------------------------------------------------

df_sentiment= pd.DataFrame(cleanedDataDict[file_list[0]]["Compound"]).merge(pd.DataFrame(cleanedDataDict[file_list[1]]["Compound"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[2]]["Compound"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[3]]["Compound"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[4]]["Compound"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[5]]["Compound"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[6]]["Compound"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[7]]["Compound"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[8]]["Compound"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[9]]["Compound"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[10]]["Compound"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[11]]["Compound"]), how = "outer", 
                                    left_index = True, right_index = True).merge(pd.DataFrame(cleanedDataDict[file_list[12]]["Compound"]), how = "outer", 
                                    left_index = True, right_index = True)



#*********************************************************************************************************
# calculate means for each row of compound value withtout na value into a new columns
tweet_sentiment= []
for Index in list(df_sentiment.index):
    tweet_sentiment.append(df_sentiment.ix[Index].mean(skipna = True))

df_sentiment['sentiment_compound'] = tweet_sentiment


#-----------------------------------------------------merge twitter data---------------------------------------------------------------------------------------


df_Twitter = pd.DataFrame(df_sentiment['sentiment_compound']).merge(pd.DataFrame(df_tweet_count['Tweet_count']), how = "outer", 
                                                       right_index = True, left_index = True)
# save it as CSV
df_Twitter.to_csv("df_Twitter.csv")
