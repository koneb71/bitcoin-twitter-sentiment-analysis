import csv
from feature_extraction import bag_of_words
from random import shuffle
#from nltk import classify
from nltk import NaiveBayesClassifier



# print(len(pos_tweets), len(neg_tweets))



# test_set = pos_tweets[:12937] + neg_tweets[:3000]
# train_set = pos_tweets[12937:] + neg_tweets[3000:]


# print(len(test_set),  len(train_set))
# classifier = NaiveBayesClassifier.train(all_train_set)


class BitCoinTweetClassifier(object):
    def __init__(self):
        self.pos_tweets = []
        self.neg_tweets = []
        self.neu_tweets = []
        self.all_train_set = []
        self.classifier = []

    def train(self):
        # with open('pos_tweet.csv', encoding="utf8", mode='r') as pos_tweet:
        with open('datasets/pos_tweet.csv', mode='r') as pos_tweet:
            pos = csv.DictReader(pos_tweet, delimiter=',')
            for ptweet in pos:
                self.pos_tweets.append((bag_of_words(ptweet['tweet']), 'positive'))

        # with open('neg_tweet.csv', encoding="utf8", mode='r') as neg_tweet:
        with open('datasets/neg_tweet.csv', mode='r') as neg_tweet:
            neg = csv.DictReader(neg_tweet, delimiter=',')
            for ntweet in neg:
                self.neg_tweets.append((bag_of_words(ntweet['tweet']), 'negative'))

        # with open('neg_tweet.csv', encoding="utf8", mode='r') as neu_tweet:
        # with open('neg_tweet.csv', mode='r') as neu_tweet:
        #     neu = csv.DictReader(neu_tweet, delimiter=',')
        #     for neutweet in neu:
        #         self.neu_tweets.append((bag_of_words(neutweet['tweet']), 'neutral'))

        shuffle(self.pos_tweets)
        shuffle(self.neg_tweets)
        #shuffle(self.neu_tweets)
        self.all_train_set = self.pos_tweets + self.neg_tweets# + self.neu_tweets
        trained = NaiveBayesClassifier.train(self.all_train_set)
        return trained
# accuracy = classify.accuracy(classifier, test_set)
# print(accuracy)
# # print(classifier.show_most_informative_features(10))
#
# from collections import defaultdict
#
# actual_set = defaultdict(set)
# predicted_set = defaultdict(set)
#
# actual_set_cm = []
# predicted_set_cm = []
#
# for index, (feature, actual_label) in enumerate(test_set):
#     actual_set[actual_label].add(index)
#     actual_set_cm.append(actual_label)
#
#     predicted_label = classifier.classify(feature)
#
#     predicted_set[predicted_label].add(index)
#     predicted_set_cm.append(predicted_label)
#
# from nltk.metrics import precision, recall, f_measure, ConfusionMatrix
#
# print('pos precision:', precision(actual_set['pos'], predicted_set['pos']))  # Output: pos precision: 0.762896825397
# print('pos recall:', recall(actual_set['pos'], predicted_set['pos']))  # Output: pos recall: 0.769
# print('pos F-measure:', f_measure(actual_set['pos'], predicted_set['pos']))  # Output: pos F-measure: 0.76593625498
#
# print('neg precision:', precision(actual_set['neg'], predicted_set['neg']))  # Output: neg precision: 0.767137096774
# print('neg recall:', recall(actual_set['neg'], predicted_set['neg'])) # Output: neg recall: 0.761
# print('neg F-measure:', f_measure(actual_set['neg'], predicted_set['neg'])) # Output: neg F-measure: 0.7640562249
