#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import twitter
import time
from langdetect import detect
import csv
import config

# Create an Api instance.
api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN,
                  access_token_secret=ACCESS_TOKEN_SECRET)

maxId = 1056286279258816512
maxLen = 0
maxLenID = 0
#tweets = []
with open('german_tweets_text_id_only.csv', 'a', encoding='utf-8', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=['id', 'text'],
                        quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()

#    fieldnames = set()
    for i in range(3600):
        query = "lang=de&q=a%20OR%20b%20OR%20c%20OR%20d%20OR%20e%20OR%20f%20OR%20g%20OR%20h%20OR%20i%20OR%20j%20OR%20k%20OR%20l%20OR%20m%20OR%20n%20OR%20o%20OR%20p%20OR%20q%20OR%20r%20OR%20s%20OR%20t%20OR%20u%20OR%20v%20OR%20w%20OR%20x%20OR%20y%20OR%20z%20-filter%3Aretweets%20-filter%3Areplies&result_type=recent&count=100"
        if maxId is not False:
            query += "&max_id="+str(maxId)
        try:
            search = api.GetSearch(raw_query=query)
            maxId = search[-1].id - 1
            #print(max_id)
            #print([s for s in search])
            for tweetDict in search:
                tweetDict = tweetDict.AsDict()
                try:
                    if detect(tweetDict['text']) != 'de':
                        continue
                except:
                    print("This text throws and error:", tweetDict['text'])
                    continue

                tweet = {}
                '''
                for key in tweetDict:
                    if key == 'user':
                        for innerKey in tweetDict[key]:
                            tweet[key + "_" + innerKey] = tweetDict[key][innerKey]
                    elif key == 'urls' or key == 'user_mentions':
                        for j in range(len(tweetDict[key])):
                            for innerKey in tweetDict[key][j]:
                                tweet[key + "_" + str(j) + "_" + innerKey] = tweetDict[key][j][innerKey]
                    else:
                        tweet[key] = tweetDict[key]
                '''
                tweet['id'] = tweetDict['id']
                tweet['text'] = tweetDict['text']
                writer.writerow(tweet)
            #           fieldnames.update(tweet.keys())
            #            tweets.append(tweet)
            print(i)
            time.sleep(2)
        except Exception as e:
            print(str(e))
            time.sleep(60)