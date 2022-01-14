from ast import parse
from itertools import count
from ntpath import join
import re
from sys import api_version
from tracemalloc import stop
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import os

class TwitterClient(object):
    #Generic Twitter Class for sentiment analysis
    def __init__(self):
        #Class constructor or initialization method
        #keys and tokens from the Twitter Dev Console
        consumer_key = os.environ.get('CONSUMER_KEY')
        consumer_secret = os.environ.get('CONSUMER_SECRET')
        access_token = os.environ.get('ACCESS_TOKEN')
        access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
        #Attempt authentication
        try:
            self.auth = OAuthHandler(consumer_key,consumer_secret)
            self.auth.set_access_token(access_token,access_token_secret)
            self.api = tweepy.API(self.auth,wait_on_rate_limit=True)
        except:
            print("Error: Authentication Failed")
            
    def clean_tweet(self,tweet):
        tweet = ' '.join(re.sub("RT","",tweet).split())
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",tweet).split())

    def get_tweet_sentiment(self,tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    def get_tweets(self,query,count):
        tweets = []
        try:
            fetched_tweets = self.api.search_tweets(q = query, count = count)
            for tweet in fetched_tweets:
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.text
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                if tweet.retweet_count > 0:
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except tweepy.errors.TweepError as e:
            print("Error: "+ str(e))

class percentages:
    def __init__(self,positive,negative,neutral,pwords,nwords):
        self.positive = positive
        self.negative = negative
        self.neutral = neutral
        self.wordcloud_neg = nwords
        self.wordcloud_pos = pwords
        

def sentimentCalc(query):
    api = TwitterClient()
    tweets = api.get_tweets(query=query, count = 200)
    ptweets = [tweet for tweet in tweets if tweet['sentiment']=='positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment']=='negative']
    netweets = [tweet for tweet in tweets if tweet['sentiment']=='neutral']
    pwords = ''
    for tweet in ptweets:
        pwords += api.clean_tweet(tweet['text'])
        pwords += ' '

    nwords = ''
    for tweet in ntweets:
        nwords += api.clean_tweet(tweet['text'])
        nwords += ' '

    return percentages(100*len(ptweets)/len(tweets),100*len(ntweets)/len(tweets),100*len(netweets)/len(tweets),pwords,nwords)