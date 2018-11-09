# -*- coding: utf-8 -*-
import json
import sys
import requests

import time
import tweepy
import codecs

from ML.twitter_stream_listener import TwitterStreamListener
from ML.sentiment_analysis import TwitterSentimentAnalysis

sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')

from settings import *
from db import store_mentions, store_sentiments

# Twitter Credentials
auth = tweepy.OAuthHandler(CUSTOMER_KEY, CUSTOMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


class TwitterBot:
    def __init__(self, cashtag):
        self.api = tweepy.API(auth)
        self.cashtag = cashtag

    def bitcoin_price(self):
        # Requesting the real-time bitcoin price url
        data = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json").json()
        return data['bpi']['USD']['rate_float']

    def run(self):
        listener = TwitterStreamListener()
        sentiment_analyzer = TwitterSentimentAnalysis()
        stream = tweepy.Stream(auth=auth, listener=listener)
        stream.filter(track=['$btcusd', '#bitcoin', 'bitcoin'], async=True)

        while True:
            time.sleep(60)
            print(listener.get_number_of_mentions())

            positive_sentiment = 0
            negative_sentiment = 0

            if listener.get_number_of_mentions() > 0:
                tweets = sentiment_analyzer.get_sentiment(listener.get_mentions())

                # picking positive tweets from tweets
                ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']

                # picking negative tweets from tweets
                ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']

                # get number per sentiments
                positive_sentiment = len(ptweets)
                negative_sentiment = len(ntweets)

            # Storing to Database
            price = self.bitcoin_price()

            id = store_mentions('bitcoin', listener.get_number_of_mentions(), price)
            store_sentiments(positive_sentiment, negative_sentiment, id)

            # Reset number of mentions
            listener.reset_counter()
