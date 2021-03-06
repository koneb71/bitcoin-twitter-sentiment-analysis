import csv

file = 'bitcointweets.csv'
neg_tweet = []
pos_tweet = []
neutral_tweet = []
with open(file, encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        if row['sentiment'] == "positive":
            pos_tweet.append(row)
        if row['sentiment'] == "negative":
            neg_tweet.append(row)
        if row['sentiment'] == "neutral":
            neutral_tweet.append(row)

with open('datasets/pos_tweet.csv', encoding="utf8", mode='w') as pos_file:
    fieldnames = ['tweet', 'sentiment']
    writer = csv.DictWriter(pos_file, fieldnames=fieldnames)

    writer.writeheader()
    for pos in pos_tweet:
        writer.writerow(pos)

with open('datasets/neg_tweet.csv', encoding="utf8", mode='w') as neg_file:
    fieldnames = ['tweet', 'sentiment']
    writer = csv.DictWriter(neg_file, fieldnames=fieldnames)

    writer.writeheader()
    for neg in neg_tweet:
        writer.writerow(neg)

with open('datasets/neutral_tweet.csv', encoding="utf8", mode='w') as neu_file:
    fieldnames = ['tweet', 'sentiment']
    writer = csv.DictWriter(neu_file, fieldnames=fieldnames)

    writer.writeheader()
    for neu in neutral_tweet:
        writer.writerow(neu)