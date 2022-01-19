from ast import parse
from itertools import count
from ntpath import join
import re
from sys import api_version
from time import perf_counter
from tracemalloc import stop
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import os
import string
from wordcloud import STOPWORDS

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
        stopwords = set(STOPWORDS)
        tweet = tweet.lower()
        tweet = re.sub("rt @[A-Za-z0-9_]+","", tweet)
        tweet = re.sub("@[A-Za-z0-9_]+","", tweet)
        tweet = re.sub("#[A-Za-z0-9_]+","", tweet)
        tweet = re.sub(r"http\S+", "", tweet)
        tweet = re.sub(r"www.\S+", "", tweet)
        tweet = re.sub(r"won\'t", "will not", tweet)
        tweet = re.sub(r"can\'t", "can not", tweet)
        tweet = re.sub(r"n\'t", " not", tweet)
        tweet = re.sub(r"\'re", " are", tweet)
        tweet = re.sub(r"\'s", " is", tweet)
        tweet = re.sub(r"\'d", " would", tweet)
        tweet = re.sub(r"\'ll", " will", tweet)
        tweet = re.sub(r"\'t", " not", tweet)
        tweet = re.sub(r"\'ve", " have", tweet)
        tweet = re.sub(r"\'m", " am", tweet)
        tweet = re.sub('[()!?]', ' ', tweet)
        tweet = re.sub('\[.*?\]',' ', tweet)
        tweet = re.sub("[^a-z0-9]"," ", tweet)
        tweet = tweet.split()
        tweet = [w for w in tweet if not w in stopwords]
        tweet = " ".join(word for word in tweet)
        return tweet

    def get_tweet_sentiment(self,tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
    
    def get_tweets(self,query):
        tweets = []
        try:
            fetched_tweets = tweepy.Cursor(self.api.search_tweets, q=query, lang = "en").items(300)
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
        except tweepy.errors.TweepyException as e:
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
    tweets = api.get_tweets(query=query)
    ptweets = [tweet for tweet in tweets if tweet['sentiment']=='positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment']=='negative']
    netweets = [tweet for tweet in tweets if tweet['sentiment']=='neutral']
    pwords_array = []
    for tweet in ptweets:
        pwords_array += api.clean_tweet(tweet['text']).split()
    pfreq = [pwords_array.count(i) for i in pwords_array]
    pwords_dict = dict(zip(pwords_array,pfreq))
    pwords = []
    for key in pwords_dict:
        pwords.append({'text':key,'value':pwords_dict[key]})

    nwords_array = []
    for tweet in ntweets:
        nwords_array += api.clean_tweet(tweet['text']).split()
    nfreq = [nwords_array.count(i) for i in nwords_array]
    nwords_dict = dict(zip(nwords_array,nfreq))
    nwords = []
    for key in nwords_dict:
        nwords.append({'text':key,'value':nwords_dict[key]})

    return percentages(100*len(ptweets)/len(tweets),100*len(ntweets)/len(tweets),100*len(netweets)/len(tweets),pwords,nwords)