
# Group Project for UI Smart Devices Class- 2022 Centennial College
# PLEASE READ!!!
# This code contains private API keys that should not be shared.
# Please DO NOT SHARE THIS PROJECT.
# I will revoke the API keys after grading.
# The API has a limit of 2500 requests every 15 minutes.
# Last Modified: 15-04-2022 by Peyman Talkhekar
# This program helps with analyzing sentiment for a certain word in twitter
# Import Libraries
from textblob import TextBlob
import tweepy
import matplotlib.pyplot as plt
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tqdm import tqdm
API_Key='NHDK1lphgFAWCEQSLA4BoXQ3n'
API_Key_Secret='n8LxFpMMfhEqHjaukMokmZOeOBO61FestjSoWMF4UAmTqvn0O3'
Access_Token='947932236569108480-YHp02hCdCrHPSOKGX68vC9SD1KV5cAz'
Access_Token_Secret='LY5qs0qd06g5h6aLiRlODXHuOG35GPn5SYtUhVyRCHDU5'
auth=tweepy.OAuthHandler(API_Key,API_Key_Secret)
auth.set_access_token(Access_Token, Access_Token_Secret)
api=tweepy.API(auth)
# this functions calculates percentage
def percent(part, whole):
    return 100*float(part)/float(whole)


key=input("please enter keyword you want to search")
numoftweet=int(input('please enter the number of tweets you want to go through'))
tweets= tweepy.Cursor(api.search_tweets, q=key).items(numoftweet)
positive = 0
negative=0
neutral=0
polarity=0
tweet_list=[]
neutral_list = []
negative_list = []
positive_list = []
for tweet in tqdm(tweets, desc='Retrieving Data...', ascii=False, ncols=75, total=numoftweet):
    # print(tweet.text)
    tweet_list.append(tweet.text)
    analysis=TextBlob(tweet.text)
    score=SentimentIntensityAnalyzer().polarity_scores(tweet.text)
    neg=score['neg']
    nue=score['neu']
    pos=score['pos']

    polarity+=analysis.sentiment.polarity
    if neg>pos:
        negative_list.append(tweet.text)
        negative+=1
    elif pos>neg:
        positive_list.append(tweet.text)
        positive+=1
    elif pos==neg:
        neutral_list.append(tweet.text)
        neutral+=1
positive=percent(positive,numoftweet)
negative=percent(negative, numoftweet)
neutral = percent(neutral, numoftweet)
polarity = percent(polarity, numoftweet)
positive = format(positive, '.1f')
negative = format(negative, '.1f')
neutral = format(neutral, '.1f')


#  In the section below, we will make a DF out of our lists.
tweet_list=pd.DataFrame(tweet_list)
tweet_list.drop_duplicates(inplace=True)
neutral_list=pd.DataFrame(neutral_list)
neutral_list.drop_duplicates(inplace=True)
negative_list=pd.DataFrame(negative_list)
negative_list.drop_duplicates(inplace=True)
positive_list=pd.DataFrame(positive_list)
positive_list.drop_duplicates(inplace=True)
print('total tweets {},\nNegative:{},\nPositive:{},\nNeutral: {}\n'.format(len(tweet_list),len(negative_list), len(positive_list), len(neutral_list)))


# Creating a pie chart
label=['Positive ['+str(positive)+'%]', 'Neutral ['+ str(neutral)+'%]', 'Negative ['+str(negative)+'%]']
SIZE=[positive, neutral, negative]
colors=['Green', 'Blue', 'Red']
patches, texts=plt.pie(SIZE, colors=colors, startangle=90)
plt.style.use('default')
plt.legend(label)
plt.title('Sentiment  analysis for :  {}'.format(key))
plt.axis('equal')
plt.show()
