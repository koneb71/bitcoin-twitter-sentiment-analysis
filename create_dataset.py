import csv

file = 'bitcointweets.csv'
neg_tweet = []
pos_tweet = []
with open(file, encoding="utf8") as fh:
    rd = csv.DictReader(fh, delimiter=',')
    for row in rd:
        if row['sentiment'] == "positive":
            pos_tweet.append(row)
        if row['sentiment'] == "negative":
            neg_tweet.append(row)

with open('pos_tweet.csv', encoding="utf8", mode='w') as pos_file:
    fieldnames = ['tweet', 'sentiment']
    writer = csv.DictWriter(pos_file, fieldnames=fieldnames)

    writer.writeheader()
    for pos in pos_tweet:
        writer.writerow(pos)

with open('neg_tweet.csv', encoding="utf8", mode='w') as neg_file:
    fieldnames = ['tweet', 'sentiment']
    writer = csv.DictWriter(neg_file, fieldnames=fieldnames)

    writer.writeheader()
    for neg in neg_tweet:
        writer.writerow(neg)