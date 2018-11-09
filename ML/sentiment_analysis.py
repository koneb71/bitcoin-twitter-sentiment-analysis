import re
import tweepy
# from textblob import TextBlob
from feature_extraction import bag_of_words
from training import BitCoinTweetClassifier


class TwitterSentimentAnalysis(object):
    '''
    Generic Twitter Class for sentiment analysis.
    '''
    def __init__(self):
        self.tweet_classifier = BitCoinTweetClassifier()
        self.classifier = self.tweet_classifier.train()

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        '''
        tweet_set = bag_of_words(self.clean_tweet(tweet))
        return self.classifier.classify(tweet_set)

    def get_sentiment(self, fetched_tweets):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []

        try:
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet

                if not isinstance(tweet, str):
                    tweet = re.split('<(.*?)>', tweet)[0]

                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet)

                # appending parsed tweet to tweets list
                if parsed_tweet in tweets:  # check if it already analyzed
                    pass
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            print("Error : " + str(e))
