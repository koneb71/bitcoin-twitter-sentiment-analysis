import csv
from feature_extraction import bag_of_words
from random import shuffle
from nltk import classify
from nltk import NaiveBayesClassifier

pos_tweets = []
with open('pos_tweet.csv', encoding="utf8", mode='r') as pos_tweet:
    pos = csv.DictReader(pos_tweet, delimiter=',')
    for ptweet in pos:
        pos_tweets.append((bag_of_words(ptweet['tweet']), 'pos'))

neg_tweets = []
with open('neg_tweet.csv', encoding="utf8", mode='r') as neg_tweet:
    neg = csv.DictReader(neg_tweet, delimiter=',')
    for ntweet in neg:
        neg_tweets.append((bag_of_words(ntweet['tweet']), 'neg'))

#print(len(pos_tweets), len(neg_tweets))

shuffle(pos_tweets)
shuffle(neg_tweets)

test_set = pos_tweets[:12937] + neg_tweets[:3000]
train_set = pos_tweets[12937:] + neg_tweets[3000:]

#print(len(test_set),  len(train_set))

classifier = NaiveBayesClassifier.train(train_set)
accuracy = classify.accuracy(classifier, test_set)
print(accuracy)
print(classifier.show_most_informative_features(10))