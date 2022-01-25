import snscrape.modules.twitter as sntwitter
from ast import parse
from itertools import count
from ntpath import join
import re
from sys import api_version
from time import perf_counter
from tracemalloc import stop
from textblob import TextBlob
import os
import string
from wordcloud import STOPWORDS


class TwitterClient(object):
    #Generic Twitter Class for sentiment analysis
    def __init__(self):
        self.maxTweets = 500

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
            i=0
            for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                parsed_tweet = {}
                parsed_tweet['text'] = tweet.content
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.content)
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
                    i+=1
                if i>=self.maxTweets:
                    break
            return tweets
        except:
            print("Error")

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
        if key not in query.lower():
            pwords.append({'text':key,'value':pwords_dict[key]})

    nwords_array = []
    for tweet in ntweets:
        nwords_array += api.clean_tweet(tweet['text']).split()
    nfreq = [nwords_array.count(i) for i in nwords_array]
    nwords_dict = dict(zip(nwords_array,nfreq))
    nwords = []
    for key in nwords_dict:
        if key not in query.lower():
            nwords.append({'text':key,'value':nwords_dict[key]})

    return percentages(100*len(ptweets)/len(tweets),100*len(ntweets)/len(tweets),100*len(netweets)/len(tweets),pwords,nwords)