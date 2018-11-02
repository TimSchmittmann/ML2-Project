#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import pandas as pd
import numpy as np
import editdistance

def remove_header_rows(csv_to_fix, read_ext, write_ext):
    with open(csv_to_fix+read_ext, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        tweets = {}
        with open(csv_to_fix+write_ext, 'w', encoding='utf-8', newline='', buffering=1) as fixedcsv:
            writer = csv.writer(fixedcsv, delimiter=';',
                            quoting=csv.QUOTE_MINIMAL)
            for row in reader:
                if row[0] == 'tweet_id':
                    print(row)
                    continue
                tweets[row[0]] = row
            print(tweets)
            for tweet in tweets:
                writer.writerow(tweet)

def remove_duplicates(csv_to_fix, read_ext, write_ext):
    tweets = pd.read_csv(csv_to_fix+read_ext, header=0, encoding='utf-8', delimiter=';');
    print(tweets.shape)
    tweets = tweets.drop_duplicates(['tweet_full_text'])
    print(tweets.shape)
    tweets = tweets.drop_duplicates(['tweet_id'])
    print(tweets.shape)
    tweets.to_csv(csv_to_fix+write_ext, index=False, sep=';', encoding='utf-8', quoting=csv.QUOTE_MINIMAL, line_terminator='\r\n')

def sort_by_tweet_id(csv_to_fix, read_ext, write_ext):
    tweets = pd.read_csv(csv_to_fix+read_ext, header=0, index_col=0, encoding='utf-8', delimiter=';');
    tweets = tweets.sort_index(ascending=False)
    tweets.to_csv(csv_to_fix+write_ext, index=True, sep=';', encoding='utf-8', quoting=csv.QUOTE_MINIMAL, line_terminator='\r\n')

def remove_by_levenshtein(csv_to_fix, read_ext, write_ext):
    tweets = pd.read_csv(csv_to_fix+read_ext, header=0, index_col=0, encoding='utf-8', delimiter=';');
    for i in range(len(tweets.index)):
        print(i)
        duplicates = tweets[tweets['tweet_full_text'].apply(lambda x: int(editdistance.eval(tweets.iloc[i,0], x)) / len(x) < 0.05)]
        if len(duplicates.index) > 1:
            print(duplicates)


csv_to_fix = "data/emoji_tweets/all_emoji_tweets_02_11_18"
read_ext = "_sorted_3.csv"
write_ext = "_levenshtein_4.csv"
# remove_header_rows(csv_to_fix, read_ext, write_ext)
# remove_duplicates(csv_to_fix, read_ext, write_ext)
# sort_by_tweet_id(csv_to_fix, read_ext, write_ext)
remove_by_levenshtein(csv_to_fix, read_ext, write_ext)