# encoding: utf-8
import json
import sys

import tweepy
import codecs

sys.stdout = codecs.getwriter("iso-8859-1")(sys.stdout, 'xmlcharrefreplace')


class TwitterStreamListener(tweepy.StreamListener):
    def __init__(self):
        super(TwitterStreamListener, self).__init__()
        self.mention_counter = []

    # def on_status(self, status):
    #     self.mention_counter.append(status.text)

    def on_data(self, data):
        self.mention_counter.append(json.loads(data)["text"])

    def reset_counter(self):
        self.mention_counter = []

    def get_mentions(self):
        return self.mention_counter

    def get_number_of_mentions(self):
        return len(self.mention_counter)

    def on_error(self, status):
        print status
